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
df_号段 = pd.read_excel(data_path + file2 ,encoding='utf-8') 
df_支局1 = pd.read_excel(data_path + 支局数据1 ,encoding='utf-8') 
df_支局1 = df_支局1[['网元','区县','乡镇_街道']]
df_支局2 = pd.read_excel(data_path + 支局数据2 ,encoding='utf-8') 
df_支局2 = df_支局2[['网元','区县','乡镇_街道']]
df_支局 = df_支局1.append(df_支局2)

df_tmp = df_tmp[(df_tmp['场景类型'] != '高速公路') & (df_tmp['场景类型'] != '汽车客运站')& (df_tmp['场景类型'] != '火车站')& (df_tmp['场景类型'] != '高铁')]

df_tmp = df_tmp.sort_values(by='总流量',ascending = False) # 按时间顺序升序排列  

df_tmp['前7位']  = df_tmp['手机号'].map(lambda x:x[0:7])
df_tmp = pd.merge(df_tmp,df_号段,how = 'left' , on = '前7位' )
df_tmp = df_tmp[df_tmp['曲靖本地号段'] != '曲靖']

df_去重复 = df_tmp[['手机号','总流量']]
df_去重复['总流量'] =  df_去重复['总流量'].astype(int)
df_去重复 = pd.pivot_table(df_去重复, index=['手机号'], 
                                      values =['总流量'], 
                                      aggfunc = {'总流量':np.sum})     
df_去重复 = df_去重复.reset_index()
df_去重复.drop('index',axis = 1,inplace = True)

df_tmp.drop('总流量',axis = 1,inplace = True)
df_最终 = pd.merge(df_去重复,df_tmp,how = 'left' , on = '手机号' )
df_最终 = df_最终.sort_values(by='手机号',ascending = True) # 按时间顺序升序排列  
df_最终 = df_最终.reset_index()
df_最终['网元'] = df_最终['小区'].map(lambda x:x.split('_')[0]) 
df_最终 = pd.merge(df_最终,df_支局,how = 'left' , on = '网元' )



with pd.ExcelWriter(out_path + '返乡数据.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_最终.to_excel(writer,'曲靖返乡数据') 

