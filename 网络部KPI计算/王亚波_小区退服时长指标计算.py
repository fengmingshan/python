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

df_break = df_break.iloc[:9,8:15]
df_break.columns
df_break['AB类退服时长'] = (
        df_break['A类小区总数.1'] *
        df_break['A类平均退服时长'] +
        df_break['B类小区总数.1'] *
        df_break['B类平均退服时长']
        )\
        /(df_break['A类小区总数.1'] + df_break['B类小区总数.1'])
df_break['AB类退服时长'] = df_break['AB类退服时长'].map(lambda x:round(x,2))
df_break['区县.1'] = df_break['区县.1'].map(lambda x:x[:2])
df_break.set_index('区县.1',inplace =True)
df_break.columns
dict_ab = df_break['AB类退服时长'].to_dict()
dict_cd = df_break['CD类平均退服时长']
全市AB =(sum(
        df_break['A类小区总数.1'] *
        df_break['A类平均退服时长']) +\
        sum(df_break['B类小区总数.1'] *
        df_break['B类平均退服时长']
        ))\
        /(sum(df_break['A类小区总数.1']) + sum(df_break['B类小区总数.1']))
全市CD =sum(
        df_break['CD类小区总数.1'] *
        df_break['CD类平均退服时长'])\
        /sum(df_break['CD类小区总数.1'])
print('\n'*2)
print('AB类退服：',全市AB)
print('CD类退服：',全市CD)