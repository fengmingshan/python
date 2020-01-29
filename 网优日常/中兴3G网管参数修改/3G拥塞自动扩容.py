# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:07:03 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

path = 'D:/3G拥塞自动扩容'
os.chdir(path)
def  calc_CE(num):
    if num <= 250 :
        ce_num = 4
    elif 250 < num <=1000 :
        ce_num = (int(num/250)+1)*4
    elif 1000 < num <= 2000 :
        ce_num = 16
    elif 2000 < num <= 3000 :
        ce_num = 32
    elif 3000 < num :
        ce_num = 64
    return ce_num

files = os.listdir(path)
for file in files:
    df_tmp = pd.read_excel('./' + file,skiprows = 3 ,nrows =1)
    if 'CE不足导致的拥塞' in df_tmp.columns:
        bloking_file = file
    df_tmp = pd.read_excel('./' + file ,nrows =1)
    if '1X_CE' in df_tmp.columns:
        ce_file = file

df_bloking = pd.read_excel('./' + bloking_file,skiprows = 3)

df_ce = pd.read_excel('./' + ce_file)

df_bloking = df_bloking[df_bloking['CE不足导致的拥塞'] > 10]
df_bloking['BTS_no'] = df_bloking['BTS'].map(lambda x:int(x.split(' ')[0]))
df_bloking['add_CE_num'] = df_bloking['CE不足导致的拥塞'].map(lambda x:calc_CE(x))
df_bloking = df_bloking[['BTS_no','add_CE_num']]
df_bloking.set_index('BTS_no',inplace =True)
bloking_dict = df_bloking['add_CE_num'].to_dict()

df_ce['new_1X_CE'] = df_ce['站号'].map(bloking_dict)
df_ce = df_ce[~df_ce['new_1X_CE'].isnull()]
df_ce.reset_index(inplace =True)
df_ce['new_1X_CE'] = df_ce['1X_CE'] + df_ce['new_1X_CE']
df_ce['new_1X_CE'] = df_ce['new_1X_CE'].map(int)

with open('d:/增加CE指令.txt','w') as f:
    for i in range(len(df_ce)):
        line1 ='APPLY CMRIGHT:SYSTEM = {bts};'.format(bts = df_ce.loc[i,'站号'])
        line2 ='SET CELICENSE:POS="{bts}",CELICENSENUM1X={ce1x};'.format(bts = df_ce.loc[i,'站号'],ce1x = df_ce.loc[i,'new_1X_CE'])
        f.writelines(line1+'\n')
        f.writelines(line2+'\n')