# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:56:47 2019

@author: Administrator
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR 
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime


import time

#登录页面
url = r'http://135.32.99.19'

driver=webdriver.Ie()
driver.get(url)
time.sleep(60)

#username = driver.find_element_by_name('login_name')
#username.click()
#username.send_keys(15334434064)
#username.send_keys(Keys.ENTER)
#password = driver.find_element_by_name('password')
#password.click()
#password.send_keys('Ab12345678')
#driver.find_element_by_link_text('获取短信密码').click() #点击短信登陆
#time.sleep(3)
#if EC.alert_is_present:
#    driver.switch_to.alert.accept()
#    print('检测到弹窗：选择 "确定"。')
#elif EC.NoAlertPresentException:
#    print('未检测到alert窗体')
#else:
#    pass
#

try:
    while True :
        time.sleep(300)
        driver.refresh()
        time.sleep(0.5)
        if EC.alert_is_present:
            driver.switch_to.alert.accept()
            print('检测到弹窗：选择 "确定"。')
        elif EC.NoAlertPresentException:
            print('未检测到alert窗体')
        else:
            pass
        current_time = str(datetime.today()).split('.')[0]
        print("4A系统保持在线! : " + current_time)  
        
except KeyboardInterrupt:
    print(u'检测到CTRL+C,准备退出程序!') 
    driver.close()
