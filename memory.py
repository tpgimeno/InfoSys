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