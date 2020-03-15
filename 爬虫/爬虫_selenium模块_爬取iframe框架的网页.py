# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:20:53 2018

@author: Administrator
"""
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
#支持多种浏览器
#browser=webdriver.Chrome()
#browser=webdriver.Firefox()
#browser=webdriver.PhantomJS()
#browser=webdriver.Safari()
#browser=webdriver.Edge() 

#url=r'http://ynszxc.gov.cn/S1/S176/S190/S201/S27594/' 
url=r'http://ynszxc.gov.cn/S1/S176/S190/S196/S34864/S34865/Default.shtml#'
browser=webdriver.PhantomJS()
#browser=webdriver.Chrome()

try:
    browser.get(url)
    browser.switch_to_frame('IframeText')
    wait=WebDriverWait(browser,1)
    wait.until(EC.presence_of_element_located((By.ID,'text')))
    print(browser.page_source)
finally:
    browser.quit()  

try:
    browser=webdriver.Chrome()
    browser.get(url)
    wait=WebDriverWait(browser,10)
    browser.switch_to.frame('current') #切换到id为iframeResult的frame

    tag1=browser.find_element_by_id('place')
    print(tag1)
    tag2=browser.find_element_by_id('text') #报错，在子frame里无法查看到父frame的元素
    print(tag2)

finally:
    browser.quit() 
    

#1. webDriver.Close() - Close the browser window that the driver has focus of //关闭当前焦点所在的窗口
#2. webDriver.Quit() - Calls dispose //调用dispose方法
#3. webDriver.Dispose() Closes all browser windows and safely ends the session 关闭所有窗口，并且安全关闭session

