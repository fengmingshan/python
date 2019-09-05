# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 17:34:07 2019

@author: Administrator
"""

import sys
import os

a = sys.argv

path_list = sys.argv[0].split('/')

path = ''
for i in range(0,len(path_list)-1):
    path = path + path_list[i] + '/'

files= os.listdir(path)

for file in files:
    print(file)