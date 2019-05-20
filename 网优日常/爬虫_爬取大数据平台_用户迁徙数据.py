# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 16:23:22 2019

@author: Administrator
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR 
from datetime import datetime

import time

url = r'http://135.32.102.28:9090/cas/login?service=http%3A%2F%2F135.32.102.28%3A9090%2Fportal%2Fpure%2FFrame.action%3Bjsessionid%3DDFF547524D3F1378977FB37E06DA4FB5%3Bjsessionid%3D1510A4DACE6F9FD3ACE1F9FBBAD7BC7A%3Bjsessionid%3D03FA57C96E08A39102699285F09A5DA1#'

driver = webdriver.Chrome()
driver.get(url)

username = driver.find_element_by_name('username')
username.click()
username.send_keys('qj_fengmingshan')

password = driver.find_element_by_name('password')
password.click()
password.send_keys('Ynctc$123')

driver.implicitly_wait(10)

report_url = driver.find_element_by_id('biCustom')
report_url.click()

driver.switch_to_window(driver.window_handles[1])
driver.switch_to_frame('noIframe')


