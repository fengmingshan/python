# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:53:31 2019

@author: Administrator
"""
import pandas as pd 
import os


data_path = r'D:\test\中兴基站信息' + '\\'

files = os.listdir(data_path)

月汇总 = pd.DataFrame()

month_list = ['2016-10','2016-11','2016-12','2017-01','2017-02','2017-03','2017-04','2017-05','2017-06','2017-07','2017-08','2017-09','2017-10',] 
for month in month_list:
    tmp_file = []
    for file in files:
        if month in file :
            tmp_file.append(file)
    for file  in tmp_file:
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
        df_维护量.loc[0,'月份'] = month
        df_维护量.loc[0,'室分数量'] = len(长高室分)
        df_维护量.loc[0,'宏站数量'] = len(长高宏站)
        df_维护量.loc[1,'公司'] = '长讯'
        df_维护量.loc[1,'月份'] = month
        df_维护量.loc[1,'室分数量'] = len(长讯室分)
        df_维护量.loc[1,'宏站数量'] = len(长讯宏站)
    
        月汇总 = 月汇总.append(df_维护量)
with  pd.ExcelWriter(data_path  + '中兴基站数量统计.xlsx')  as writer:  #输出到excel
    月汇总.to_excel(writer, '中兴基站数量统计',index =False)             
    




 

