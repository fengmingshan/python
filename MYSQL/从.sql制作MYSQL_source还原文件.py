# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 11:11:23 2020

@author: Administrator
"""

import os

path = r'C:\Users\Administrator\Desktop'
os.chdir(path)

name = 'report'

with open('report.sql',encoding ='utf-8') as f:
    content = f.readlines()
    for i,line in enumerate(content):
        if 'SET FOREIGN_KEY_CHECKS=0;' in line:
            no = i+1
content.insert(no,'USE {};'.format(name))
content.insert(no,'CREATE DATABASE IF NOT EXISTS {};'.format(name))
content.insert(no,'DROP DATABASE IF EXISTS {};'.format(name))




with open('report_new.sql','w',encoding ='utf-8') as f:
    for line in content:
        f.writelines(line)