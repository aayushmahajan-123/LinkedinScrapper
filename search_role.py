from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import re
from bs4 import BeautifulSoup
import pyautogui

def search(driver,role,location="worldwide"):
    role.replace(" ","%20")
    location.replace(" ", "%20")
    link = "https://www.linkedin.com/jobs/search/?keywords="+role+"&location="+location
    driver.get(link)
    return [driver,link]


def scroller():
    i = 6
    for x in range(i):
        pyautogui.scroll(-10, x=370, y=320)
        i+=1
        sleep(3)

def scroller2():
    i = 70
    for x in range(i):
        pyautogui.scroll(-10, x=800, y=450)
        i += 1
        sleep(1)

def create_next_link(link,no_of_jobs,count):
    if count+25>=no_of_jobs:
        return ["-",count]
    else:
        count+=25
        if count==100:  ### keep it 1000 for full fledged
            return ["-",count]
        return [link + "&start=" + str(count),count]