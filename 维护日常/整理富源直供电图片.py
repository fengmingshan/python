# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 09:02:21 2021

@author: Administrator
"""

import os
import pandas as pd
from shutil import copyfile

path = r'D:\2021年工作\2021年1月电费三家互结\2021年1月各县上报\富源'
os.chdir(path)

names = ['富源十八连山母猪山530325908000000107',
     '富源县大河镇白马村委会王家脑包村530325908000000153',
     '富源后所镇双诺村530325908000000151',
     '富源黄泥河电信大楼530325908001900092',
     '富源大河镇530325908000000001',
     '富源中安新电信大楼530325908001900091']

monthes  = ['2020年1月',
            '2020年2月',
            '2020年3月',
            '2020年4月',
            '2020年5月',
            '2020年6月',
            '2020年7月',
            '2020年8月',
            '2020年9月',
            '2020年10月',
            '2020年11月',
            '2020年12月']

source_file = []
for root,dirs,files, in os.walk(r'D:\2021年工作\2021年1月电费三家互结\2021年1月各县上报\富源\2020年直'):
    for name in files:
        source_file.append(os.path.join(root, name))

for name in names:
    os.mkdir('./富源/'+name)
    for month in monthes:
        os.mkdir('./富源/'+ name +'/' + month)
        tmp_files = [x for x in source_file if month in x]
        for file in tmp_files:
            copyfile(file,'./富源/'+ name +'/' + month + '/' + os.path.basename(file) )




