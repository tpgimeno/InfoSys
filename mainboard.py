from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import *
import re

import time
path = "C:\Webdriver\chromedriver-win64\chromedriver.exe"


def normalizeString(string):
    cleanString = re.sub(r'[^a-zA-Z0-9()\s]', '', string)
    return cleanString

def getMainBoardInfo(name):
    googleSite = "https://www.google.es/"
    cService = webdriver.ChromeService(executable_path=path)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=cService, options=options)
    driver.get(googleSite)
    time.sleep(2)
    acceptCookies = driver.find_element(By.ID, "L2AGLb")
    acceptCookies.click()
    time.sleep(1)
    search_input = driver.find_element(By.ID, "APjFqb")
    search_input.send_keys(name.strip() + " specs")
    time.sleep(1)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)
    search_result = driver.find_elements(By.CLASS_NAME, "MjjYud a")    
    for item in search_result:
        if(item.text.find("www.asus.com") > -1):
            if(item.text.find("techspecs")):
                item.click()
                break
    time.sleep(3)
    acceptCookies = driver.find_element(By.CSS_SELECTOR, "#cookie-policy-info > div > div.cookie-btn-box > div.btn-asus.btn-ok.btn-read-ck")
    acceptCookies.click()
    time.sleep(1)
    rows = driver.find_elements(By.CLASS_NAME, "TechSpec__rowTable__1LR9D")
    
    data = {}
    index = 0 
    for row in rows:
        if(rows.index(row) > 1):            
            title = row.find_elements(By.CLASS_NAME, "rowTableTitle")            
            rowData = row.find_elements(By.CLASS_NAME, "TechSpec__rowTableItems__KYWXp")                    
            for item in rowData:
                feature = item.text.splitlines()                
                if(name in feature):
                    index = rowData.index(item)                    
            
            for item in rowData:
                if(item != rowData[0]):
                    data[title[0].text] = rowData[index].text
            

    return data

