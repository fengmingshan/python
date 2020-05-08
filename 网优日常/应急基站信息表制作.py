# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:40:16 2020

@author: Administrator
"""

import pandas as pd
import os

work_path = r'C:\Users\Administrator\Desktop\曲靖基站信息更新'
os.chdir(work_path)
col = ['州市', '县区', '基站名称', '基站类型', '经度', '纬度']
files = os.listdir(work_path)
files

df_list = []
df1 = pd.read_excel('3G基站信息表-曲靖20191217.xls')
df1.columns
df1.CELLNAME.head(5)
df1['州市'] = '曲靖'
df1['县区'] = df1['CELLNAME'].map(lambda x:x[:2])
df1['县区'][df1['县区']=='华夏'] = '麒麟'
df1.县区.unique()
df1['基站名称'] = df1['CELLNAME'].map(lambda x:x.split('_')[0])
df1['基站类型'] = '3G'
df1['经度'] = df1['LON']
df1['纬度'] = df1['LAT']
df1 = df1[['州市', '县区', '基站名称', '基站类型', '经度', '纬度']]
df1 = df1.drop_duplicates('基站名称',keep = 'first')
df_list.append(df1)

df2 = pd.read_excel('华为高铁C网.xls')
df2.columns
df2.小区名.head(5)
df2['州市'] = '曲靖'
df2['县区'] = df2['BBU名称'].map(lambda x:x.split('QJ')[1][:2])
df2.县区.unique()
df2['基站名称'] = df2['小区名'].map(lambda x:x.split('-')[0])
df2['基站类型'] = '3G'
df2 = df1[['州市', '县区', '基站名称', '基站类型', '经度', '纬度']]
df2 = df2.drop_duplicates('基站名称',keep = 'first')
df_list.append(df2)

df3 = pd.read_excel('华为网元报表_20190415_143939.xlsx')
df3.columns
df3.网元名称.head(5)
df3['州市'] = '曲靖'
df3['县区'] = df3['网元名称'].map(lambda x:x.split('QJ')[1][:2])
df3.县区.unique()
df3['基站名称'] = df3['网元名称'].map(lambda x:x.split('QJ')[1].split('_')[0])
df3['基站类型'] = '4G-1800M'
df3 = df1[['州市', '县区', '基站名称', '基站类型', '经度', '纬度']]
df3 = df3.drop_duplicates('基站名称',keep = 'first')
df_list.append(df3)

df4 = pd.read_excel('曲靖电信LTE1.8G工参2020413.xls')
df4.columns
df4 = df4[['ENODEBID','CELLID']]
df4['ECI'] = df4['ENODEBID']*256 + df4['CELLID']
df4['厂家'] = '中兴'

df4.CELLID.head(5)
df4['州市'] = '曲靖'
df4['县区'] = df4['ENODEBName'].map(lambda x:x[:2])
df4.县区.unique()
df4['基站名称'] = df4['CELLNAME'].map(lambda x:x.split('_')[2])
df4['基站类型'] = '4G-1800M'
df4 = df1[['州市', '县区', '基站名称', '基站类型', '经度', '纬度']]
df4 = df4.drop_duplicates('基站名称',keep = 'first')
df_list.append(df4)

df5 = pd.read_excel('曲靖电信LTE800M工参2020413.xls')
df5.columns
df5.CELLID.head(5)
df5 = df5[['ENODEBID','CELLID']]
df5['ECI'] = df5['ENODEBID']*256 + df4['CELLID']
df5['厂家'] = '中兴'

df5['州市'] = '曲靖'
df5['县区'] = df5['ENODEBName'].map(lambda x:x[:2])
df5.县区.unique()
df5['基站名称'] = df5['CELLNAME'].map(lambda x:x.split('_')[2])
df5['基站类型'] = '4G-800M'
df5 = df1[['州市', '县区', '基站名称', '基站类型', '经度', '纬度']]
df5 = df5.drop_duplicates('基站名称',keep = 'first')
df_list.append(df5)

df6 = pd.read_excel('爱立信云南曲靖电信工参表20200407.xlsx')
df6.cellId.head(5)
df6 = df6[['eNBId','cellId']]
df6['ECI'] = df6['eNBId']*256 + df6['cellId']
df6.rename(columns = {'eNBId':'ENODEBID','cellId':'CELLID'},inplace=True)
df6['厂家'] = '爱立信'
df6['SiteName(Chinese)'].head(5)
df6['州市'] = '曲靖'
df6['县区'] = df6['SiteName(Chinese)'].map(lambda x:x[:2])
df6.县区.unique()
df6['县区'][df6['县区']=='曲靖'] = df6['SiteName(Chinese)'][df6['县区']=='曲靖'].map(lambda x:x[2:4])
df6['基站名称'] = df6['SiteName(Chinese)']
df6['基站类型'] = '4G-800M'
df6['经度'] = df6['longitude']
df6['纬度'] = df6['latitude']
df6 = df6[['州市', '县区', '基站名称', '基站类型', '经度', '纬度']]
df6 = df6.drop_duplicates('基站名称',keep = 'first')
df_list.append(df6)

df_all = pd.concat(df_list,axis = 0)
with pd.ExcelWriter('曲靖无线基站清单_2020-04-15.xlsx') as f:
    df_all.to_excel(f,'曲靖无线基站清单',index =False)

li = [df4,df5,df6]
df_eci = pd.concat(li,axis =0)

with pd.ExcelWriter('全市ECI.xlsx') as f:
    df_eci.to_excel(f,'全市ECI',index = False)