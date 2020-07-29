# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:47:08 2020

@author: Administrator
"""

from selenium import webdriver

driver = webdriver.PhantomJS()
url = 'http://180.153.49.130:9000/baf/jsp/uiframe/login.jsp'  # 定义url地址
driver.get(url)  # 加载url网页
response = driver.page_source  # page_source方法获得url的源代码
print(response)  # 获得sina源代码


