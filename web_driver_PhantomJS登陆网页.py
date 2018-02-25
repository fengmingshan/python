# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 11:29:23 2018

@author: Administrator
"""

import requests            #导入requests库  
from bs4 import BeautifulSoup   #导入BeautifulSoup库  
from requests.exceptions import RequestException     #导入requests库中的错误和异常字段   
import json                      #导入json库  
import sys
import io
from selenium import webdriver
from selenium import webdriver 
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素

#建立Phantomjs浏览器对象，括号里是phantomjs.exe在你的电脑上的路径
browser = webdriver.PhantomJS()

#登录页面
url = r'http://123.126.34.146:20000/uac/web3/jsp/login/login.jsp'

# 访问登录页面
browser.get(url)

# 等待一定时间，让js脚本加载完毕
browser.implicitly_wait(3)

#输入用户名
username = browser.find_element_by_name('loginName')
username.send_keys('yn-qujdxwh')

#输入密码
password = browser.find_element_by_id('passwd_input_placeholder')
password.send_keys('1234@dxWX')


#点击“登录”按钮
login_button = browser.find_element_by_id('login_btn')
login_button.submit()
browser.implicitly_wait(3)

#打印网页源代码
x=browser.page_source
y=browser.page_source.encode('utf-8').decode()

browser.quit()

'''
带cookies登陆知乎
'''
from selenium import webdriver
from requests import Session
from time import sleep
req = Session()
req.headers.clear() 
wd = webdriver.Chrome() 
zhihuLogInUrl = 'https://www.zhihu.com/signin'
wd.get(zhihuLogInUrl)
wd.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/span').click()
wd.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[1]/input').send_keys('username') 
wd.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/input').send_keys('password')
sleep(10) #手动输入验证码 
wd.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/form/div[2]/button').submit() 
sleep(10)#等待Cookies加载
cookies = wd.get_cookies()
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value'])


