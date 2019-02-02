# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:42:20 2018

@author: Administrator
"""
import time

import sys
import os
import shutil

path = r'd:\test' + '\\'
path_new = r'd:\test\new' + '\\'

cTime = "2016-01-15 16:07:02"
mTime = "2016-01-15 17:08:02"
file1 = r'd:\test\3G基站信息表-曲靖201601.xls'
file2 = r'd:\test\电信LTE工参201601.xls'


cTime_t =time.mktime(time.strptime(cTime,'%Y-%m-%d %H:%M:%S')) 
mTime_t =time.mktime(time.strptime(mTime,'%Y-%m-%d %H:%M:%S')) 

os.utime(file1, (cTime_t, mTime_t))
os.utime(file2, (cTime_t, mTime_t))
