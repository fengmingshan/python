# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 10:31:03 2019

@author: Administrator
"""
import pandas as pd 
import numpy as np
import os

# =============================================================================
# 设置环境变量
# =============================================================================
data_path = r'd:\test' + '\\'
out_path = r'd:\test' + '\\'

file1 = '返乡数据0129.csv'
file2 = '曲靖号段.xls'
支局数据1 = 'zte_eNode_name.xls'
支局数据2 = '爱立信关联支局.xlsx'

df_tmp = pd.read_csv(data_path + file1 ,sep=';',encoding='gbk',engine = 'python',dtype = str) 
for col in df_tmp.columns:
    df_tmp[col] = df_tmp[col].map(lambda x:x.replace('nan',''))
df_tmp.drop_duplicates( inplace=True)  
  
df_号段 = pd.read_excel(data_path + file2 ,encoding='utf-8') 
df_支局1 = pd.read_excel(data_path + 支局数据1 ,encoding='utf-8') 
df_支局1 = df_支局1[['网元','区县','乡镇_街道']]
df_支局2 = pd.read_excel(data_path + 支局数据2 ,encoding='utf-8') 
df_支局2 = df_支局2[['网元','区县','乡镇_街道']]
df_支局 = df_支局1.append(df_支局2)
df_支局.drop_duplicates(inplace=True)

df_tmp = df_tmp[(df_tmp['场景类型'] != '高速公路') & (df_tmp['场景类型'] != '汽车客运站')& (df_tmp['场景类型'] != '火车站')& (df_tmp['场景类型'] != '高铁')]

df_tmp = df_tmp.sort_values(by='总流量',ascending = False) # 按时间顺序升序排列  

df_tmp['前7位']  = df_tmp['手机号'].map(lambda x:x[0:7])
df_tmp = pd.merge(df_tmp,df_号段,how = 'left' , on = '前7位' )
df_tmp = df_tmp[df_tmp['曲靖本地号段'] != '曲靖']

df_tmp['手机号'] = df_tmp['手机号'].astype(str)
df_tmp['总流量'] = df_tmp['总流量'].astype(int)
df_tmp['总流量'] = df_tmp['总流量'].map(lambda x:x/1024)

df_tmp = df_tmp.sort_values(by=['手机号','总流量'],ascending = False) # 按时间顺序升序排列  
df_tmp.drop_duplicates('手机号', 'first',inplace=True)

df_tmp = df_tmp.reset_index()
df_tmp.drop('index',axis = 1,inplace = True)
df_tmp['网元'] = df_tmp['小区'].map(lambda x:x.split('_')[0]) 
df_tmp['网元'] = df_tmp['网元'].astype(int)
df_tmp = pd.merge(df_tmp,df_支局,how = 'left' , on = '网元' )
df_tmp = df_tmp[['区县','乡镇_街道','小区','手机号','号码归属省','号码归属市','总流量','终端品牌','终端型号','日期','号码归属省','号码归属市','上周常驻城市','上周常驻区域']]
df_tmp.rename(columns={'小区':'基站名称','总流量':'总流量(MB)','终端品牌':'手机品牌','终端型号':'手机型号'},inplace =True)
df_tmp.fillna('-',inplace = True)

区县列表 = list(set(df_tmp['区县']))
df_区县 = pd.DataFrame()
for 区县 in 区县列表:
    df_区县 = df_tmp[df_tmp['区县'] == 区县]  
    with pd.ExcelWriter(out_path + 区县 + '_4G返乡数据.xlsx') as writer: #不用保存和退出，系统自动会完成
        df_区县.to_excel(writer, 区县 + '4G返乡数据',index = False) 

