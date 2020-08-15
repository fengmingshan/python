# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:32:05 2020

@author: Administrator
"""
import pandas as pd
import os

path = r'D:\_python小程序\网络部KPI指标计算'
os.chdir(path)

df_break = pd.read_excel('真实全市小区退服汇总_2020-7（上报）.xlsx',skiprows =1)

df_break = df_break.iloc[:9,:5]
df_break.columns
df_break.set_index('区县',inplace =True)
dict_ab = df_break['AB类小区平均退服时长(达标值: <130分钟)'].to_dict()
dict_cd = df_break['CD类小区平均退服时长(达标值: <300分钟)'].to_dict()

全市AB =(sum(
        df_break['AB类小区总数'] *
        df_break['AB类小区平均退服时长(达标值: <130分钟)']
        ))\
        /sum(df_break['AB类小区总数'])
全市CD =sum(
        df_break['CD类小区总数'] *
        df_break['CD类小区平均退服时长(达标值: <300分钟)'])\
        /sum(df_break['CD类小区总数'])

df_res = pd.DataFrame()
df_res['区县'] = ['麒麟区', '沾益县', '富源县', '宣威市', '会泽县', '马龙县', '陆良县', '师宗县', '罗平县','全市']
df_res['AB类平均退服时长'] = df_res['区县'].map(dict_ab)
df_res['CD类平均退服时长'] = df_res['区县'].map(dict_cd)
df_res.loc[9,'AB类平均退服时长'] = 全市AB
df_res.loc[9,'CD类平均退服时长'] = 全市CD

with pd.ExcelWriter('退服时长.xlsx') as f:
    df_res.to_excel(f,index = False)
