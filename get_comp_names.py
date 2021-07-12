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


def readtxt_addunique(my_set,text_filename):
    with open(text_filename) as f:
        for line in f:
            line.rstrip('\n')
            line.lstrip('\n')
            my_set.add(line)

    return my_set

def write_data(my_set,text_filename):

    with open(text_filename, 'w') as f:
        for x in my_set:
            x.rstrip('\n')
            x.lstrip('\n')
            f.write(x)
            f.write('\n')

    f.close()


driver = webdriver.Firefox(executable_path="./drivers/geckodriver")
driver.get('http://linkedin.com')
driver.maximize_window()
driver.find_element_by_id("session_key").send_keys("aayushmahajan@yahoo.com")
driver.find_element_by_id("session_password").send_keys("<enter password here>")
driver.find_element_by_class_name("sign-in-form__submit-button").click()
sleep(2)

driver.get("https://www.linkedin.com/in/aayush-mahajan-b046b0163/detail/interests/companies/")
search_role.scroller2()


comp_list = driver.find_element_by_class_name("entity-list.row")
companies = comp_list.find_elements_by_class_name("entity-list-item")
print(len(companies))
unique_companies=set()
for list_item in companies:
    comp_name = list_item.find_element_by_class_name("pv-entity__summary-title-text").get_attribute("innerText")
    unique_companies.add(comp_name)

readtxt_addunique(unique_companies,"search_string")
print(len(unique_companies))
open("search_string",'w').close()
write_data(unique_companies,"search_string")


