# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:13:01 2019

@author: Administrator
"""# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 20:53:31 2019

@author: Administrator
"""
import pandas as pd 
import os


data_path = r'D:\test\爱立信基站信息' + '\\'

files = os.listdir(data_path)

month_list = ['2017-05','2017-06','2017-07','2017-08','2017-09','2017-10',] 
月汇总 = pd.DataFrame()

for month in month_list:
    tmp_file = []
    for file in files:
        if month in file :
            tmp_file.append(file)
    
    for file  in tmp_file:
        df_tmp = pd.read_excel(data_path + file ,encoding='utf-8')
        df_tmp = df_tmp[['地市','Site Name(Chinese)']]
        df_tmp['区县'] =  df_tmp['Site Name(Chinese)'].map(lambda x:x[0:2])
        宏站 = list(set(df_tmp['Site Name(Chinese)']))
    
        长高宏站 = [x for x in 宏站 if '麒麟' in x or '沾益' in x or '马龙' in x or '陆良' in x or '宣威' in x or '会泽' in x ]
        长讯宏站 = [x for x in 宏站 if '富源' in x or '陆良' in x or '师宗' in x]
    
        df_维护量 = pd.DataFrame(columns = ('公司','月份','室分数量','宏站数量'))
        df_维护量.loc[0,'公司'] = '长高'
        df_维护量.loc[0,'月份'] = month
        df_维护量.loc[0,'宏站数量'] = len(长高宏站)
        df_维护量.loc[1,'公司'] = '长讯'
        df_维护量.loc[1,'月份'] = month
        df_维护量.loc[1,'宏站数量'] = len(长讯宏站)
        月汇总 = 月汇总.append(df_维护量)

with  pd.ExcelWriter(data_path  + '爱立信基站数量统计.xlsx',index =False)  as writer:  #输出到excel
    月汇总.to_excel(writer, '爱立信基站数量统计')             

    




 



