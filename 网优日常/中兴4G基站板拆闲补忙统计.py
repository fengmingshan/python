# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 16:35:10 2020

@author: Administrator
"""

import pandas as pd
import os

path = 'D:/2020年工作/2020年1月L800M网络扩容基带板拆闲补忙'
os.chdir(path)
if not os.path.exists('./结果输出'):
    os.mkdir('./结果输出')

files = os.listdir('./data')
file_content = []
for file in files:
    df_tmp = pd.read_excel('./data/' + file , sheet_name = 'FiberCable',header=1)
    df_tmp.drop([0,1],inplace =True)
    file_content.append(df_tmp)
df = pd.concat(file_content,axis =0)
df.reset_index(inplace =True,drop=True)

with pd.ExcelWriter('./结果输出/合并后文件.xlsx') as writer:
    df.to_excel(writer,index = False)