from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import *
import re

import time
path = "C:\Webdriver\chromedriver-win64\chromedriver.exe"

def normalizeString(string):
    cleanString = re.sub(r'[^a-zA-Z0-9()\s]', '', string)
    return cleanString

def getCpuIntelData(name):
    intelsite = "https://ark.intel.com/content/www/xl/es/ark/search.html?_charset_=UTF-8&q="
    cService = webdriver.ChromeService(executable_path=path)
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(service=cService, options=options)
    driver.get(intelsite)
    time.sleep(5)
    cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookies_button.click()
    time.sleep(1)
    search_field = driver.find_element(By.ID, "ark-searchbox")
    search_field.send_keys(name)
    time.sleep(1)
    search_button = driver.find_element(By.ID, "search-products-submit")
    search_button.click()
    time.sleep(2)
    cpuList = driver.find_elements(By.CLASS_NAME, "search-result")
    if(cpuList):
        itemLinks = driver.find_elements(By.CLASS_NAME, 'result-title a')
        itemLinks[len(itemLinks)-1].click()
    time.sleep(1)
    result = driver.find_elements(By.TAG_NAME, "section")
    infolength = len(result)
    data = []  
    dataList = []     
    for i in range(4, infolength - 4):        
        section = result[i].text.split("\n")  
        dataList.append(section)
    
    for item in dataList:
        for h in range(0, len(item)):
            if(len(item[h]) > 0):
                if(h != 0):
                    data.append(item[h])

    dictData = {}
    for i in range(0, len(data) - 1,2):
        key = normalizeString(data[i]).strip()
        dictData[key] = data[i+1]
    
    
    
    return dictData







