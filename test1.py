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
import scrape_job_data as sjd
import pandas as pd
from xlsxwriter import Workbook
import calendar
import time


dataframes = []
search_strings = []

def excel_writer():
    n = len(dataframes)

    ts = calendar.timegm(time.gmtime())

    writer = pd.ExcelWriter('jobs@'+str(ts)+'.xlsx', engine='xlsxwriter')

    x = 0
    for x in range(n):
        dataframes[x].to_excel(writer,sheet_name=search_strings[x])
        x+=1

    writer.save()

def main2(driver,role,loc):
    if loc=="/":
        loc="worldwide"

    if role=="":
        return

    search_strings.append(str(role) + "_" + str(loc))
    temp = search_role.search(driver, role,loc)
    driver = temp[0]
    link = temp[1]
    glink = link

    sleep(3)
    pageSource = driver.page_source
    lxml_soup = BeautifulSoup(pageSource, 'lxml')

    try:
        results = lxml_soup.find('small', {'class': 'display-flex t-12 t-black--light t-normal'}).get_text().strip().split()[0]
        no_of_jobs = int(results.replace(',', ''))
        print(no_of_jobs)
    except AttributeError:
        return

    count = 0

    job_id = []
    job_title = []
    company_name = []
    location = []
    job_link = []

    while link != "-":

        search_role.scroller()

        job_list = driver.find_element_by_class_name("jobs-search-results__list")
        jobs = job_list.find_elements_by_class_name("jobs-search-results__list-item")
        print(len(jobs))

        lists = sjd.scrape_basic_info(jobs)
        sleep(1)

        job_id=job_id+lists[0]
        job_title = job_title + lists[1]
        company_name = company_name + lists[2]
        location = location + lists[3]
        job_link = job_link + lists[4]

        l = search_role.create_next_link(glink, no_of_jobs, count)
        link = l[0]
        count = l[1]
        if link != "-":
            driver.get(link)
        sleep(3)


    df = pd.DataFrame({'JobId': job_id, 'JobTitle': job_title, 'CompName': company_name, 'Location': location, 'JobLink': job_link})
    print(df)
    dataframes.append(df)


def main():
    driver = webdriver.Firefox(executable_path="./drivers/geckodriver")
    driver.get('http://linkedin.com')
    driver.maximize_window()
    driver.find_element_by_id("session_key").send_keys("aayushmahajan@yahoo.com")
    driver.find_element_by_id("session_password").send_keys("aayush123!!!")
    driver.find_element_by_class_name("sign-in-form__submit-button").click()
    sleep(2)
    driver.get("https://www.linkedin.com/jobs/")
    sleep(2)


    with open('search_string') as f:
        for line in f:
            role = "/"
            loc ="/"
            temp = line.split("#")
            if len(temp)==2:
                role,loc = temp[0],temp[1]
            elif len(temp)==1:
                role = temp[0]
            main2(driver,role,loc)

    excel_writer()



if __name__ == "__main__":
    main()

