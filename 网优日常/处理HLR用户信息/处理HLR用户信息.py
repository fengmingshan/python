# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 09:10:07 2020

@author: Administrator
"""

import pandas as pd
import os
from functools import reduce
from tqdm import tqdm
work_path = r'D:/用户数据库/3G_HRL/'
os.chdir(work_path)

df_qj = pd.read_excel('曲靖号段_2020-04-20.xls')

files = [x for x in os.listdir(work_path) if '.txt' in x]

content = [open(x,'r').read() for x in tqdm(files)]
content_all = reduce(lambda x,y: x+y,content)

lines = content_all.split('\n')

number_list = [x.split()[0][2:-3] for x in tqdm(lines) if x!='']

imsi_list = ['46003'+x.split()[2] for x in tqdm(lines) if x!='']

df_res = pd.DataFrame({'号码':number_list, 'IMSI':imsi_list})

df_res['号段'] = df_res['号码'].map(lambda x:int(x[:7]))
df_res = df_res[df_res['号段'].isin(df_qj['NUM'])]

with open('曲靖用户号码对应IMSI_2020-04.csv','w',encoding = 'utf-8',newline = '') as f:
    df_res.to_csv(f,index = False)

