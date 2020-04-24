# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:39:09 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os


def read_csv_partly(file):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=100000)
    for df_tmp in file_data:
        yield df_tmp


work_path = 'D:/_python/python/网优日常/修改套餐失效日期脚本'
os.chdir(work_path)
if not os.path.exists('结果输出'):
    os.mkdir('结果输出')

files = os.listdir()
user_files = [x for x in files if ('.py' not in x and os.path.isfile(x))]
print('共发现{}个原始文件!'.format(len(user_files)))

list_df_file = []
for i,file in enumerate(user_files):
    list_df_tmp = []
    for j,df_tmp in enumerate(read_csv_partly(file)):
        try:
            list_df_tmp.append(df_tmp)
        except:
            print("读取文件失败！")
        print('读取:{}W 行!'.format((j+1)*10))
    df_file = pd.concat(list_df_tmp, axis=0)
    print('完成第{}个文件，共{}行!'.format(i+1,len(df_file)))
    list_df_file.append(df_file)

if len(list_df_file) > 1:
    df = pd.concat(list_df_file, axis=0)
else :
    df = df_file

df_file.columns