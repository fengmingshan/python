# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:56:47 2019

@author: Administrator
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR 
from datetime import datetime

import time

#登录页面
url = r'http://135.32.99.19'

driver=webdriver.Ie()
driver.get(url)
username = driver.find_element_by_name('login_name')
username.click()
username.send_keys(15334434064)
username.send_keys(Keys.ENTER)
password = driver.find_element_by_name('password')
password.click()
password.send_keys('Ab12345678')
driver.find_element_by_link_text('获取短信密码').click()
time.sleep(3)
driver.switch_to_alert().accept()  # 针对IE提出的提示信息点击重试按钮
driver.find_element_by_name('smsPassword').click()

# 等待一定时间，让js脚本加载完毕
driver.implicitly_wait(30)
try:
    while True :
        time.sleep(30)
        driver.refresh()
        driver.switch_to_alert().accept()  # 针对IE提出的提示信息点击重试按钮
        current_time = str(datetime.today()).split('.')[0]
        print("4A系统保持在线! : " + current_time)          
except KeyboardInterrupt:
    print('检测到CTRL+C,准备退出程序!') 
    driver.close()
