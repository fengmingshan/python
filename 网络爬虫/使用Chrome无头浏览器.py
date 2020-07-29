# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:09:58 2020

@author: Administrator
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--user-data-dir d:/test/')

my_driver = webdriver.Chrome(executable_path=r'C:\ProgramData\Anaconda3\Scripts\chromedriver',options = options)
my_driver.get("https://www.baidu.com")
h = my_driver.page_source
print(h)

my_driver.get("https://www.zhihu.com/")
h = my_driver.page_source
print(h)

