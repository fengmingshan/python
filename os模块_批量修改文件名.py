# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 22:40:18 2018
批量修改文件名称
@author: Administrator
"""
import os
import datetime
import time

file_path = r'D:\SCTP' + '\\'
month_trans = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,
              'July':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12} # 中英文月份对照字典        


files = os.listdir(file_path)
file_list = []
for file in files:
    if '_保存' in file:
        file_list.append(file)
# 原来的文件名 filename = '2018-Mar-14_00-08-08_保存.txt'         
for filename in file_list:
    year = int(filename[0:4])
    month = month_trans[filename.split('-')[1]]  # 查月份翻译表得到数字的月份
    day = int(filename.split('-')[2][0:2])
    hour = int(filename.split('_')[1][0:2])
    minute = int(filename.split('_')[1][3:5])
    second = int(filename.split('_')[1][-2:])
    day_tuple = tuple(datetime.date(year, month, day).timetuple())
    tm_wday =day_tuple[6]    # 周几
    tm_yday = day_tuple[7]    # 一年中的第几天
    tm_isdst = 0    # 是否夏令时    
    struct_time = (year,month,day,hour,minute,second,tm_wday,tm_yday,tm_isdst)
    strftime_time = time.strftime('%Y-%m-%d %H:%M:%S',struct_time) # 转换采集时间为正常时间格式
    os.rename(file_path + filename,file_path + strftime_time.replace(':','.')+'_保存.txt')


