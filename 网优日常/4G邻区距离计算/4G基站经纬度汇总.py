# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:05:16 2020

@author: Administrator
"""

import pandas as pd
import os
import numpy as np

path = r'D:\_python小程序\4G邻区距离计算'
os.chdir(path)

# 汇总基站信息表
df_zte800 = pd.read_excel('./曲靖电信LTE800M工参20200519.xls')
df_zte1800 = pd.read_excel('./曲靖电信LTE1.8G工参20200521.xls')
df_eric800 = pd.read_excel('./爱立信云南曲靖电信工参表20200507.xlsx')

df_zte800['CELL'] = df_zte800.ENODEBID.map(str) + '_' + df_zte800.CELLID.map(str)
df_zte800['CELLNAME'] = df_zte800['CELLNAME'].map(lambda x:x.split('_')[2]+x.split('_')[1])
df_zte800.rename(columns = {'LONC':'LON','LATC':'LAT'},inplace =True)
df_zte800 = df_zte800[['CELL','CELLNAME','LON','LAT']]

df_zte1800['CELL'] = df_zte1800.ENODEBID.map(str) + '_' + df_zte1800.CELLID.map(str)
df_zte1800['CELLNAME'] = df_zte1800['CELLNAME'].map(lambda x:x.split('_')[2]+x.split('_')[1])
df_zte1800.rename(columns = {'LONC':'LON','LATC':'LAT'},inplace =True)
df_zte1800 = df_zte1800[['CELL','CELLNAME','LON','LAT']]

df_eric800.columns
df_eric800['CELL'] = df_eric800.eNBId.map(str) + '_' + df_eric800.cellId.map(str)
df_eric800['CELLNAME'] = df_eric800['SiteName(Chinese)'] + df_eric800['cellId'].map(str)
df_eric800.rename(columns = {'longitude':'LON','latitude':'LAT'},inplace =True)
df_eric800 = df_eric800[['CELL','CELLNAME','LON','LAT']]

df_all = pd.concat([df_zte800,df_zte1800,df_eric800], axis =0)
df_all.reset_index(drop = True,inplace =True)

with open('./4G基站经纬度.csv','w',newline='') as f:
    df_all.to_csv(f,index =False)



