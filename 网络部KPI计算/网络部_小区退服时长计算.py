# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:32:05 2020

@author: Administrator
"""
import pandas as pd
import os

path = r'D:\_python小程序\网络部KPI指标计算'
os.chdir(path)

df_break = pd.read_excel('真实全市小区退服汇总_2020-06（上报）.xlsx',skiprows =1)

df_break = df_break.iloc[:9,:7]

df_break['AB类退服时长'] = (
        df_break['A类小区总数'] *
        df_break['A类小区平均退服时长(达标值: <115分钟)'] +
        df_break['B类小区总数'] *
        df_break['B类小区平均退服时长(达标值: <150分钟)']
        )\
        /(df_break['A类小区总数'] + df_break['B类小区总数'])
df_break['AB类退服时长'] = df_break['AB类退服时长'].map(lambda x:round(x,2))
df_break['区县'] = df_break['区县'].map(lambda x:x[:2])
df_break.set_index('区县',inplace =True)
df_break.columns
dict_ab = df_break['AB类退服时长'].to_dict()
dict_cd = df_break['CD类小区平均退服时长(达标值: <300分钟)']
全市AB =(sum(
        df_break['A类小区总数'] *
        df_break['A类小区平均退服时长(达标值: <115分钟)']) +\
        sum(df_break['B类小区总数'] *
        df_break['B类小区平均退服时长(达标值: <150分钟)']
        ))\
        /(sum(df_break['A类小区总数']) + sum(df_break['B类小区总数']))
全市CD =sum(
        df_break['CD类小区总数'] *
        df_break['CD类小区平均退服时长(达标值: <300分钟)'])\
        /sum(df_break['CD类小区总数'])

df_res = pd.DataFrame()
df_res['区县'] = ['麒麟', '沾益', '富源', '宣威', '会泽', '马龙', '陆良', '师宗', '罗平','全市']
df_res['AB类'] = df_res['区县'].map(dict_ab)
df_res['CD类'] = df_res['区县'].map(dict_cd)
with pd.ExcelWriter('退服时长.xlsx') as f:
    df_res.to_excel(f,index = False)
