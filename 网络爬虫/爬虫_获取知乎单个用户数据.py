# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:58:32 2020

@author: Administrator
"""

from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

url = 'https://www.zhihu.com/people/haili-9-70/'
driver.get(url)
sleep(1)

rlts = driver.find_elements_by_class_name("Tabs-meta")
nums1 = [rlt.text for rlt in rlts]

rlts = driver.find_elements_by_class_name("NumberBoard-itemValue")
nums2 = [rlt.text for rlt in rlts]

rlt = {}
rlt["用户"] = url
rlt["回答"] = nums1[0]
rlt["视频"] = nums1[1]
rlt["提问"] = nums1[2]
rlt["文章"] = nums1[3]
rlt["专栏"] = nums1[4]
rlt["想法"] = nums1[5]
rlt["收藏"] = nums1[6]
rlt["关注了"] = nums2[0]
rlt["关注者"] = nums2[1]
rlt["日期"] = str(datetime.now())[:-7]

driver.quit()

print(rlt)