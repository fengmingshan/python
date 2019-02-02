# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:53:31 2019

@author: Administrator
"""
import pandas as pd 
import os
import numpy as np

month = '2017-11'
data_path = r'D:\test' + '\\'

files = os.listdir(data_path)
file_list = []
for file in files :
    if  month in file and '爱立信' in file:
        file_list.append(file)

df_汇总 = pd.DataFrame()
for file  in file_list:
    df_tmp = pd.read_excel(data_path + file ,encoding='utf-8')
    df_tmp = df_tmp[['RRU中文名','区县']]
    宏站 = list(set(df_tmp['RRU中文名']))
    
    长高宏站 = [x for x in 宏站 if ('麒麟' in x or '沾益' in x or '马龙' in x or '陆良' in x or '宣威' in x or '会泽')]
    长讯宏站 = [x for x in 宏站 if ('富源' in x or '陆良' in x or '师宗' in x)]
    
    df_维护量 = pd.DataFrame(columns = ('公司','月份','宏站数量'))
    df_维护量.loc[0,'公司'] = '长高'
    df_维护量.loc[0,'月份'] = month
    df_维护量.loc[0,'宏站数量'] = len(长高宏站)
    df_维护量.loc[1,'公司'] = '长讯'
    df_维护量.loc[1,'月份'] = month
    df_维护量.loc[1,'宏站数量'] = len(长讯宏站)

with  pd.ExcelWriter(data_path + '代维维护量_爱立信' + '_' + month + '.xlsx')  as writer:  #输出到excel
    df_维护量.to_excel(writer,'维护量',index=False) 


 

