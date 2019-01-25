# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:53:31 2019

@author: Administrator
"""
import pandas as pd 
import os


data_path = r'D:\test' + '\\'

files = os.listdir(data_path)

#month_list = ['201704','201705','201706','201707','201708','201709','201710',] 
month = '201709'
月汇总 = pd.DataFrame()
tmp_file = []
for file in files:
    if month in file :
        tmp_file.append(file)

for file  in tmp_file:
    file = '电信LTE工参(L1.8G)20170930.xls'
    df_tmp = pd.read_excel(data_path + file ,encoding='utf-8')
    df_tmp = df_tmp[['CELLNAME','基站类型']]
    df_室分 = df_tmp[df_tmp['基站类型'] == '室分']
    df_室分['区县'] =  df_室分['CELLNAME'].map(lambda x:x.split('QJ')[1][0:2])
    df_室分['CELLNAME'] =  df_室分['CELLNAME'].map(lambda x:x.split('_')[2].split('QJ')[1])
    df_宏站 = df_tmp[df_tmp['基站类型'] == '宏站']
    df_宏站['区县'] =  df_宏站['CELLNAME'].map(lambda x:x.split('QJ')[1][0:2])
    df_宏站['CELLNAME'] =  df_宏站['CELLNAME'].map(lambda x:x.split('_')[2].split('QJ')[1])
    室分 = list(set(df_室分['CELLNAME']))
    宏站 = list(set(df_宏站['CELLNAME']))

    长高室分 = [x for x in 室分 if ('麒麟' in x or '沾益' in x or '马龙' in x or '陆良' in x or '宣威' in x or '会泽')]
    长高宏站 = [x for x in 宏站 if ('麒麟' in x or '沾益' in x or '马龙' in x or '陆良' in x or '宣威' in x or '会泽')]
    长讯室分 = [x for x in 室分 if ('富源' in x or '陆良' in x or '师宗' in x)]
    长讯宏站 = [x for x in 宏站 if ('富源' in x or '陆良' in x or '师宗' in x)]

    df_维护量 = pd.DataFrame(columns = ('公司','月份','室分数量','宏站数量'))
    df_维护量.loc[0,'公司'] = '长高'
    df_维护量.loc[0,'月份'] = 'month'
    df_维护量.loc[0,'室分数量'] = len(长高室分)
    df_维护量.loc[0,'宏站数量'] = len(长高宏站)
    df_维护量.loc[1,'公司'] = '长讯'
    df_维护量.loc[1,'月份'] = 'month'
    df_维护量.loc[1,'室分数量'] = len(长讯室分)
    df_维护量.loc[1,'宏站数量'] = len(长讯宏站)

月汇总 = 月汇总.append(df_维护量)
    




 

