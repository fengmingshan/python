# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:56:47 2019

@author: Administrator
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR 

import time

__browser_url = r'C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe' 
#登录页面
url = r'http://135.32.99.19'


chrome_options = Options()
chrome_options.binary_location = __browser_url

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

# 等待一定时间，让js脚本加载完毕
browser.implicitly_wait(5)

time.sleep(60)
driver.refresh()


