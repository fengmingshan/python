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
username = driver.find_element_by_name('login_name')
username.click()
username.send_keys(15334434064)
username.send_keys(Keys.ENTER)
password = driver.find_element_by_name('password')
password.click()
password.send_keys('Ab12345678')
driver.find_element_by_link_text('获取短信密码').click()
driver.find_element_by_name('smsPassword').click()


# 等待一定时间，让js脚本加载完毕
driver.implicitly_wait(30)
try:
    while True :
        time.sleep(300)
        driver.refresh()
except KeyboardInterrupt:
    print('检测到CTRL+C,准备退出程序!') 

    

