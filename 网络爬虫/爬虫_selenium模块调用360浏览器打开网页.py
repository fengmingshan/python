# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 17:26:53 2018

@author: Administrator
"""

from selenium.webdriver.chrome.options import Options  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
import time  
  
__browser_url = r'C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe'  ##360浏览器的地址  
chrome_options = Options()  
chrome_options.binary_location = __browser_url  
  
driver = webdriver.Chrome(chrome_options=chrome_options)  
driver.get('http://www.baidu.com')  