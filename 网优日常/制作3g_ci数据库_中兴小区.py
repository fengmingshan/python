# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-20 15:57:21
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-20 16:19:23

import pandas as pd
import os

data_path = 'D:/Test/3GCI数据库制作'
os.chdir(data_path)
files = os.listdir('./')

df_BSC1 = pd.DataFrame()
for file in files:
    if 'BSS1' in file:
        df_tmp  = pd.read_excel(file ,skiprows = 1, encoding = 'utf-8')
        df_BSC1 = df_BSC1.append(df_tmp)
df_BSC1['bssid'] = 'BSC1'

df_BSC2 = pd.DataFrame()
for file in files:
    if 'BSS2' in file:
        df_tmp  = pd.read_excel(file ,skiprows = 1, encoding = 'utf-8')
        df_BSC2 = df_BSC2.append(df_tmp)
df_BSC2['bssid'] = 'BSC2'

df_zte = df_BSC1.append(df_BSC2)
df_zte['区县'] = df_zte['alias_b'].apply(lambda x:x.split('QJ')[1][:2])
df_zte['全球小区号'] = df_zte['ci']
df_zte = df_zte[['bssid','区县','system','全球小区号','cellid','sid','nid','lac','pilot_pn','alias_b','base_lat_b','base_long_b','btsalias']]
with  pd.ExcelWriter( '中兴小区.xls')  as writer:  #输出到excel
    df_zte.to_excel(writer,'中兴小区',index = False)
