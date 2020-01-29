# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:42:20 2018

@author: Administrator
"""
import time

import sys
import os
import shutil
import pandas as pd
import random

path = 'D:/2019年工作/2019年9月集团无线网优工作巡查/_备查资料汇总/铁塔服务沟通会议纪要_2019'
os.chdir(path)

file_list = os.listdir('./')

date_list = ['2019-02-03', '2019-03-04', '2019-04-05', '2019-05-06',
             '2019-06-05', '2019-07-03', '2019-08-04', '2019-09-03']

for i,file in enumerate(file_list):
    aTime = date_list[i]  # 访问时间
    mTime = date_list[i]  # 修改时间
    rand_time1 = 3600*15 + 7200*random.random()
    rand_time2 = 3600*15 + 7200*random.random()

    aTime_t = time.mktime(time.strptime(aTime, '%Y-%m-%d')) + rand_time1
    mTime_t = time.mktime(time.strptime(mTime, '%Y-%m-%d')) + rand_time2
    os.utime(file, (aTime_t, mTime_t))  # 修改文件时间信息
