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
file_new = r'd:\test\基站巡检信息（模板）-1.xlsx'

os.stat(file)
shutil.copy(file, file_new)

shutil.copystat(file, file_new)

os.path.getctime(file)

a = os.path.getatime(file)
m = os.path.getmtime(file)

os.utime(file_new, (a, m))
