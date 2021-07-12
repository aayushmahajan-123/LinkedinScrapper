from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import search_role
from requests import get
from bs4 import BeautifulSoup
import re
import pyautogui
import pandas as pd
from selenium.common.exceptions import NoSuchElementException



def scrape_basic_info(jobs):
    job_id = []
    job_title = []
    company_name = []
    location = []
    job_link = []
    for job in jobs:
        try:
            temp = job.find_element_by_class_name("job-card-container")
            ji = temp.get_attribute("data-job-id")
            #print(job_id0)
            job_id.append(ji)

            jt = job.find_element_by_class_name("job-card-list__title").get_attribute("innerText")
            #print(job_title0)
            job_title.append(jt)

            cn = job.find_element_by_class_name("artdeco-entity-lockup__subtitle").get_attribute("innerText")
            #print(comp_name)
            company_name.append(cn)

            loc = job.find_element_by_class_name("artdeco-entity-lockup__caption").get_attribute("innerText")
            #print(loc)
            location.append(loc)

            jl = job.find_element_by_class_name("job-card-list__title").get_attribute("href")
            #print(jl)
            job_link.append(jl)

           # print(ji+ " " + jt+" "+cn+" "+loc+" "+jl)


        except NoSuchElementException:
            pass

    #df = pd.DataFrame({'JobId':job_id, 'JobTitle':job_title, 'CompName':company_name, 'Location':location, 'JobLink':job_link})
    return [job_id,job_title,company_name,location,job_link]

