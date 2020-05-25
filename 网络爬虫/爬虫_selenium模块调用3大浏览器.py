# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:04:02 2018

@author: Administrator
"""

#启动谷歌浏览器
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')



#启动火狐浏览器
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://www.baidu.com/')


#启动IE浏览器
from selenium import webdriver

browser = webdriver.Ie()
browser.get('http://www.baidu.com/')