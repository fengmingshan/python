# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 09:49:57 2018

@author: Administrator
"""

import os
import shutil

source_path = r'D:\3G_voltage' + '\\' 
dest_path = r'D:\电压数据备份\BSC1' + '\\' 

all_files =  os.listdir(source_path)
dest_files = os.listdir(dest_path)  
vo_file_list = []
for file in all_files:
    if '-fm-envi-info' in file :
        vo_file_list.append(file)

copy_files = []
for vofile in vo_file_list:
    if vofile not in dest_files:
        copy_files.append(vofile)

for copyfile in copy_files:
    shutil.copy(source_path + copyfile, dest_path)
print('数据采集完成：本次采集%d个文件,已入库！'% len(copy_files))
