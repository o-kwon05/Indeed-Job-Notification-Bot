#import neccesary modules

import selenium
from random import randint
from time import sleep
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException



joblist=[]
descriptionlist=[]
finallist=[]
jobdetailslist=[]
listofindex=[]
current_postings=[]


receiver_email = input("Enter Your Email:")
job_=input("Enter Job Title: ")
job=job_.replace(" ","+")
location=input("Enter location: ")

url = 'https://www.indeed.com/jobs?q={}&l={}&radius=50&sort=date&filter=0&start={}&vjk=967df61ba8042584'

#Using selenium to access Chrome
#driver = webdriver.Chrome()

#driver.get(url.format(job,location,0))#0 is page 1
#sleep(2)

#Finding the number of job postings, then mathematically finding the number of pages
#jobcount=int(driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text.split(' ')[0])
#numofpages=(jobcount//15)+1 #+1 because int division always rounds down.
#print(f"Number of Posted Jobs: {jobcount}")


def checkjobposting(job,location):

    driver = webdriver.Chrome()
    driver.get(url.format(job,location,0))#0 is page 1
    sleep(2)
    #Finding the number of job postings, then mathematically finding the number of pages
    jobcount=int((driver.find_element(By.CLASS_NAME, 'jobsearch-JobCountAndSortPane-jobCount').text.split(' ')[0]).replace(',',''))
    numofpages=(jobcount//15)+1 #+1 because int division always rounds down.
    print(f"Number of Posted Jobs: {jobcount}")
    
#Accessing each page
    for i in range(0, numofpages):
    #Accessing the link. i*10 determines what pages number
        driver.get(url.format(job,location,i*10))
    #sleep to help load all the content
        sleep(randint(1,2))
    
    
    #Class: slider_container is in every individual job listing and is the parent of all the info. elements of each job
    #.find_elements finds every single "slider_container"
        jobs = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for j in jobs:
        
        #Scrapping jobtitle (if provided) and putting it into a list
            try:
                jobtitle = j.find_element(By.CLASS_NAME,"jobTitle").text
                joblist.append(jobtitle)
            except:
            #If job title doesn't exist, catch the Exception
                joblist.append("N/A")

            try: 
                j.find_element(By.CLASS_NAME,"jcs-JobTitle").click()
                sleep(3)
                descriptionlist.append(driver.find_element(By.ID,"jobDescriptionText").text.replace("\n",""))
                jobdetailslist.append(driver.find_element(By.ID,"jobDetailsSection").text.replace("\nHere’s how the job details align with your job preferences.\nManage job preferences anytime in your profile\n.\n",":").replace("\n"," "))
            except:
                descriptionlist.append("N/A")
                jobdetailslist.append("N/A")
    finallist=list(zip(joblist,jobdetailslist))
    return finallist


def newjobpostcheck(job,location):
    global current_postings
    new_postings=checkjobposting(job,location)
    if new_postings!=current_postings and len(new_postings)>=len(current_postings):
        listofindex=(find_unique_element_index(current_postings,new_postings))
        print(listofindex)
        send_email(listofindex)
        


def find_unique_element_index(list1, list2):
    unique_indices_list2 = [i for i, item in enumerate(list2) if item not in list1]
    return unique_indices_list2


def send_email(list):
    for num in list:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'job.notification.bot@gmail.com'
        smtp_password = 'cnmn jxsm lkim xurj'
        sender_email = 'job.notification.bot@gmail.com'


    # Set up the MIMEText object

        body = "Subject: New " + job_ + " position in " + location
        body += "\n\nJob Title: " + joblist[num]
        body += "\n\nJob Detail: " + jobdetailslist[num]
        body += "\n\nJob Description: " + descriptionlist[num]

    # Establish a connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Login to the SMTP server
            server.starttls()
            server.login(smtp_username, smtp_password)

        # Send the email
            server.sendmail(sender_email, receiver_email, body.encode('utf-8'))


while True:
    current_postings=checkjobposting(job,location)
    print(current_postings)
    sleep(900)
    newjobpostcheck(job,location)

    

Software


