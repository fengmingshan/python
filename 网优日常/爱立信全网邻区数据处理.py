# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:32:01 2019

@author: Administrator
"""

import pandas as pd

data_path = r'd:\_爱立信全网邻区核查' + '\\'
eric_neighbor = r'd:\_爱立信全网邻区核查\PARA_ERBS_371.csv'
zte_neighbor = r'd:\_爱立信全网邻区核查\ZTE_neighbors.xlsx'
zte_eric800 = r'd:\_爱立信全网邻区核查\爱立信云南曲靖电信工参表20190428.xlsx'
zte_bts800 = r'd:\_爱立信全网邻区核查\曲靖电信LTE工参(L800M)20190425.xls'
zte_bts1800 = r'd:\_爱立信全网邻区核查\曲靖电信LTE工参(L1.8G)20190425.xls'

df_eric = pd.read_csv(eric_neighbor,engine = 'python')

df_eric_result = pd.DataFrame()
df_eric_result['Scell_index'] = df_eric['CELL'].map(lambda x:x.split('_')[0] + x.split('_')[1])
df_eric_result['Ncell_index'] = df_eric['EUTRANCELLRELATIONID'].map(lambda x:x.replace('46011-','').replace('-',''))
df_eric_result['relation'] = df_eric_result['Scell_index'] + '_' + df_eric_result['Ncell_index']

df_zte_result = pd.read_excel(zte_neighbor)
df_zte_result['relation'] = df_zte_result['Scell_index'].map(str) + '_' + df_zte_result['Ncell_index'].map(str)

df_all_neighbors = df_eric_result.append(df_zte_result)

df_tmp = pd.read_excel(zte_bts800)
df_zte800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_zte800['eNodeB_ID'] = df_tmp['ENODEBID']
df_zte800['Cell_name'] = df_tmp['CELLNAME']
df_zte800['Cell_index'] = df_tmp['ENODEBID'].map(str)  + df_tmp['CELLID'].map(str)
df_zte800['LON'] = df_tmp['LONC']
df_zte800['LAT'] = df_tmp['LATC']
df_zte800['azimuth'] = df_tmp['Azimuth']
df_zte800['network'] = 'L800'
df_zte800['manufacturers'] = 'ZTE'

df_tmp = pd.read_excel(zte_bts1800)
df_zte1800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_zte1800['eNodeB_ID'] = df_tmp['ENODEBID']
df_zte1800['Cell_name'] = df_tmp['CELLNAME']
df_zte1800['Cell_index'] = df_tmp['ENODEBID'].map(str)  + df_tmp['CELLID'].map(str)
df_zte1800['LON'] = df_tmp['LONC']
df_zte1800['LAT'] = df_tmp['LATC']
df_zte1800['azimuth'] = df_tmp['Azimuth']
df_zte1800['network'] = 'L1.8'
df_zte1800['manufacturers'] = 'ZTE'

df_tmp = pd.read_excel(zte_eric800)
df_eric800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_eric800['eNodeB_ID'] = df_tmp['eNBId']
df_eric800['Cell_name'] = df_tmp['Cell_name']
df_eric800['Cell_index'] =  df_tmp['Cell_index']
df_eric800['LON'] = df_tmp['longitude']
df_eric800['LAT'] = df_tmp['latitude']
df_eric800['azimuth'] = df_tmp['azimuth']
df_eric800['network'] = df_tmp['channelBandwidth'].map({'5M':'L800M', '15M':'L1.8'})
df_eric800['manufacturers'] = 'ERIC'

df_all_cells = df_zte800.append(df_zte1800).append(df_eric800)



with pd.ExcelWriter(data_path + '爱立信全网邻区输出.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_eric.to_excel(writer,'Sheet1',index =False)


