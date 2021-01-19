# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 08:03:39 2021

@author: Administrator
"""

import os
from shutil import copyfile

path = r'D:\2020年转'
os.chdir(path)

file_list = []

for root, dirs, files in os.walk(path):
    for name in files:
        file_list.append(os.path.join(root, name))

bts_names = list(set([x.split('\\')[3] for x in file_list]))
for name in bts_names:
    os.mkdir(name)

for name in bts_names:
    tmp_files = [x for x in file_list if name in x]
    monthes  = list(set([x.split('\\')[2] for x in tmp_files]))
    for month in monthes:
        os.mkdir(name + '\\' +month)
        name_fils = [x for x in tmp_files if month in x]
        for file in name_fils:
            copyfile(file,name + '\\' + month +'\\'+ os.path.basename(file))



