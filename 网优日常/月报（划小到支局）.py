# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:22:59 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import os
import xlsxwriter
from datetime import datetime

data_path = r'd:\_月报（划小到支局）' + '\\'
eric_data_path = r'd:\_月报（划小到支局）\爱立信话务' + '\\'
zte_data_path = r'd:\_月报（划小到支局）\中兴话务' + '\\'


out_path = r'd:\_月报（划小到支局）' + '\\'
eric_eNodeB = '爱立信关联支局.xlsx'
zte_eNodeB = 'eNode_name.xls'
title = 'title.xlsx'

eric_files = os.listdir(eric_data_path) 
zte_files = os.listdir(zte_data_path) 

df_eric_eNodeB = pd.read_excel(data_path + eric_eNodeB,encoding = 'utf-8')
df_zte_eNodeB = pd.read_excel(data_path + zte_eNodeB,encoding = 'utf-8')

df_4G_traffic = pd.DataFrame() #用来汇总4G话务量

df_eric_titles  = pd.read_excel(data_path + 'title.xlsx',encoding = 'utf-8')
titles = list(df_eric_titles.columns)

for file in eric_files:    
    df_tmp = pd.read_csv(eric_data_path + file,header = None,names = titles, engine = 'python', encoding = 'gbk')
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x.replace('\'',''))
    df_tmp['DATE_ID'] = df_tmp['DATE_ID'].map(lambda x:x[0:7])
    df_tmp['eNodeB'] = df_tmp['eNodeB'].map(lambda x:x.replace('\'',''))
    df_pivot = pd.pivot_table(df_tmp, index=['DATE_ID','eNodeB'],
                              values = ['Air Interface_Traffic_Volume_UL_MBytes',
                                        'Air Interface_Traffic_Volume_DL_MBytes'],                                                                         
                              aggfunc = {'Air Interface_Traffic_Volume_UL_MBytes':np.sum,
                                         'Air Interface_Traffic_Volume_DL_MBytes':np.sum })                                                                               
    df_pivot['总流量'] = df_pivot['Air Interface_Traffic_Volume_UL_MBytes'] + df_pivot['Air Interface_Traffic_Volume_DL_MBytes']
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'DATE_ID':'月份',
                             'eNodeB':'网元',
                             'Max number of UE in RRc' : 'RRC连接用户数',
                             'Air Interface_Traffic_Volume_UL_MBytes':'上行流量(MB)',
                             'Air Interface_Traffic_Volume_DL_MBytes':'下行流量(MB)'},inplace =True)
    df_pivot['网元'] = df_pivot['网元'].astype(int)
    df_pivot = pd.merge(df_pivot,df_eric_eNodeB,on = '网元',how = 'left')  
    df_4G_traffic = df_4G_traffic.append(df_pivot) 


for file in zte_files:    
    df_tmp = pd.read_csv(zte_data_path + file,skiprows = 5,engine = 'python', encoding = 'gbk')
    df_tmp['空口上行用户面流量（MByte）_1'] = df_tmp['空口上行用户面流量（MByte）_1'].map(lambda x:float(x.replace(',','')))
    df_tmp['空口下行用户面流量（MByte）_1477070755617-11'] = df_tmp['空口下行用户面流量（MByte）_1477070755617-11'].map(lambda x:float(x.replace(',','')))
    df_tmp['开始时间'] = df_tmp['开始时间'].map(lambda x:x[0:7])
    df_pivot = pd.pivot_table(df_tmp, index=['开始时间','网元'],
                              values = [ '空口下行用户面流量（MByte）_1477070755617-11',
                                        '空口上行用户面流量（MByte）_1'],                                        
                              aggfunc = {'空口下行用户面流量（MByte）_1477070755617-11':np.sum,
                                         '空口上行用户面流量（MByte）_1':np.sum})
    df_pivot['总流量'] = df_pivot['空口上行用户面流量（MByte）_1'] + df_pivot['空口下行用户面流量（MByte）_1477070755617-11']
    df_pivot = df_pivot.reset_index()
    df_pivot.rename(columns={'开始时间':'月份',
                             '空口下行用户面流量（MByte）_1477070755617-11':'下行流量(MB)',
                             '空口上行用户面流量（MByte）_1':'上行流量(MB)',
                             },inplace =True)
    df_pivot = df_pivot[['月份','网元','下行流量(MB)','上行流量(MB)','总流量']]
    df_pivot = pd.merge(df_pivot,df_zte_eNodeB,on = '网元',how = 'left')  
    df_4G_traffic = df_4G_traffic.append(df_pivot) #用来汇总4G话务量

with  pd.ExcelWriter(out_path + '4G话务量.xlsx')  as writer:  #输出到excel
    df_4G_traffic.to_excel(writer,'4G话务量')

country_list = list(set(df_4G_traffic['区县']))





