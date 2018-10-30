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

path = r'd:/test' + '//'
file_path = r'd:/test1' + '//'   #需要修改时间的文件

time_file = 'time_info.xlsx'  #时间信息文件
df_time = pd.read_excel(path + time_file, encoding = 'utf-8')  #读取时间信息文件

file_list = os.listdir(file_path)
i = 0
for file in file_list:
    aTime = str(df_time.loc[i,'aTime'])  #访问时间
    mTime = str(df_time.loc[i,'mTime'])  #修改时间
    
    aTime_t =time.mktime(time.strptime(aTime,'%Y-%m-%d %H:%M:%S')) 
    mTime_t =time.mktime(time.strptime(mTime,'%Y-%m-%d %H:%M:%S'))        
    os.utime(file_path+file, (aTime_t, mTime_t))   #修改文件时间信息
    i = i+1