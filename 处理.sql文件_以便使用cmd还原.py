# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:54:46 2020

@author: Administrator
"""

import os

path= 'D:/'
os.chdir(path)

db_name = 'rsrp_grid_09'

with open('rsrp_grid_10.sql', 'r',encoding ='utf-8') as f:
    content = f.read()
    with open('5g_bts_info_new.sql', 'w',encoding ='gbk') as f:
        f.writelines('DROP DATABASE IF EXISTS {};'.format(db_name)+'\n')
        f.writelines('CREATE DATABASE IF NOT EXISTS {};'.format(db_name)+'\n')
        f.writelines('USE {};'.format(db_name)+'\n')
        f.writelines("SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';"+'\n')
        f.writelines(content)
