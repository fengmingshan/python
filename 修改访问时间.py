# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 10:42:20 2018

@author: Administrator
"""
import time

import sys
import os
import shutil

cTime = "2011-03-19 20:07:02"
mTime = "2011-03-19 20:07:02"
file =r'd:\test\基站巡检信息（模板）.xlsx'
file_new = 

os.stat(file)
shutil.copystat(path, path_new)

cTime_t =time.mktime(time.strptime(cTime,'%Y-%m-%d %H:%M:%S')) 
mTime_t =time.mktime(time.strptime(mTime,'%Y-%m-%d %H:%M:%S')) 

os.utime(file, (cTime_t, mTime_t))
