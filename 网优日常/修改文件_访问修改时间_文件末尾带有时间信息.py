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

path = 'E:/网络运行分析月报_2019'
os.chdir(path)

file_list = os.listdir('./')

for file in file_list:
    aTime = file.split('_')[1].replace('.docx','')  #访问时间
    mTime = file.split('_')[1].replace('.docx','')   #修改时间
    rand_time1 = 3600*8 + 3600*random.random()
    rand_time2 = 3600*8 + 3600*random.random()

    aTime_t =time.mktime(time.strptime(aTime,'%Y-%m-%d')) + rand_time1
    mTime_t =time.mktime(time.strptime(mTime,'%Y-%m-%d')) + rand_time2
    os.utime(file, (aTime_t, mTime_t))   #修改文件时间信息
