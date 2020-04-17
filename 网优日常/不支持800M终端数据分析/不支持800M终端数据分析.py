# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:16:05 2020

@author: Administrator
"""

import pandas as pd
import os

work_path = r'D:\2020年工作\2020年曲靖不支持800M的终端分析'
os.chdir(work_path)
files = os.listdir()
files
df = pd.read_excel('曲靖非800用户流量top3小区_2020-04.xlsx')

df_substution = pd.read_excel('物理站址关联支局清单.xlsx')
df_substution.columns
df_substution['ENODEBID'] = df_substution['小区号'].map(lambda x:x.split('_')[0])
df_substution['CELLID'] = df_substution['小区号'].map(lambda x:x.split('_')[1])
df_substution['ENODEBID'] =df_substution['ENODEBID'].astype(int)
df_substution['CELLID'] =df_substution['CELLID'].astype(int)
df_substution['ECI'] = df_substution['ENODEBID']*256 + df_substution['CELLID']

df_substution.set_index('ECI',inplace =True)
dict_enb = df_substution['ENODEBID'].to_dict()
dict_cellid = df_substution['CELLID'].to_dict()

df_substution.set_index('小区号',inplace =True)
country_dict = df_substution['区县'].to_dict()
substution_dict = df_substution['支局'].to_dict()

df['小区'] = df['小区'].astype(str)
df['ECI'] = df['小区'].map(lambda x:x[6:])
df['ECI'] =df['ECI'].astype(int)


df['eNodeBID'] = df['ECI'].map(dict_enb)
df['CELLID'] = df['ECI'].map(dict_cellid)
df['cell_index'] = df['eNodeBID'].map(lambda x:str(x)[:-2]) +'_'+ df['CELLID'].map(lambda x:str(x)[:-2])
df['区县'] = df['cell_index'].map(country_dict)
df['支局'] = df['cell_index'].map(substution_dict)
df.columns
df_tmp = df[df['CELLID'].isnull()]
df = df[~df['CELLID'].isnull()]
df_gr = df.groupby(['号码','区县','支局','终端厂家','终端型号'],as_index=False)['流量'].sum()
df_gr.sort_values(['号码','流量'],ascending = [True,False],inplace =True)
df_gr = df_gr.groupby(['号码'],as_index=False).head(1)
df_gr['流量'] = round(df_gr['流量']/(1024*1024),1)
df_gr.rename(columns = {'流量':'流量(MB)'},inplace = True)
df_substution = df_gr.groupby(['区县','支局'],as_index = False)['号码'].count()
df_country = df_gr.groupby(['区县'],as_index = False)['号码'].count()
df_substution.rename(columns = {'号码':'数量'},inplace = True)
df_country.rename(columns = {'号码':'数量'},inplace = True)

with pd.ExcelWriter('不支持800M终端清单.xlsx') as f:
    df_country.to_excel(f,'按区县统计用户数量',index =False)
    df_substution.to_excel(f,'按支局统计用户数量',index =False)
    df_gr.to_excel(f,'号码清单',index =False)
