# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 09:39:36 2020

@author: Administrator
"""
import pandas as pd
import os
import numpy
from tqdm import tqdm


work_path = 'D:/2020年工作/2020年4月4G邻区专项优化'
os.chdir(work_path)


def calc_Distance(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)]) # 经纬度转换成弧度
    dlon = lon2-lon1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance,0)
    return distance


list_df = [pd.read_excel('./全网切换关系/'+file,header = 5) for file in os.listdir('./全网切换关系')]
df = pd.concat(list_df,axis = 0)
df['Scell'] =df['网元'].map(str) + '_' + df['小区'].map(str)
df['Ncell'] =df['邻区关系'].map(lambda x:x.split(':')[3]+'_'+x.split(':')[4])
df['ralations'] =df['Scell'] + '-' + df['Ncell']

df_1800 = pd.read_excel('./曲靖电信LTE1.8G工参2020420.xls',sheet_name = 'CXT')
df_1800.drop(['是否边界'],axis = 1, inplace = True)

df_800 = pd.read_excel('./曲靖电信LTE800M工参2020420.xls',sheet_name = 'CXT')
df_800.drop(['是否共C网', '是非边界', '逻辑根'],axis = 1, inplace = True)

df_bts = df_1800.append(df_800)
df_bts['cell_index'] = df_bts['ENODEBID'].map(str) + '_' +df_bts['CELLID'].map(str)
df_bts.set_index('cell_index',inplace = True)
name_dict = df_bts['CELLNAME'].to_dict()
with open('name_dict.txt','w') as f:
    f.write(str(name_dict))
with open('name_dict.txt','r') as f:
    name_dict = eval(f.read())
lonlat_dict = {k:(x,y) for k,x,y in zip(df_bts.index, df_bts['LONC'], df_bts['LATC'])}


df_cur_config = pd.read_excel('./全网已配置邻区_简.xlsx',enging ='python')
df_cur_config['Scell'] =df_cur_config['MEID'].map(str) + '_' + df_cur_config['CellId'].map(str)
df_cur_config['Ncell'] =df_cur_config['eNBId'].map(str) + '_' + df_cur_config['NCellId'].map(str)
df_cur_config['ralations'] =df_cur_config['Scell'] + '-' + df_cur_config['Ncell']

df_zero_handover = df_cur_config[['Scell','Ncell','ralations']][~df_cur_config['ralations'].isin(df['ralations'])]
df_zero_handover.reset_index(inplace =True)
df_zero_handover['Scell_name'] = df_zero_handover['Scell'].map(name_dict)
df_zero_handover['Scell_lon'] = df_zero_handover['Scell'].map(lambda x:lonlat_dict.get(x, default=('',''))[0])
df_zero_handover['Scell_lat'] = df_zero_handover['Scell'].map(lambda x:lonlat_dict.get(x, default=('',''))[1])
df_zero_handover['Ncell_name'] = df_zero_handover['Ncell'].map(name_dict)
df_zero_handover['Ncell_lon'] = df_zero_handover['Ncell'].map(lambda x:lonlat_dict.get(x, default=('',''))[0])
df_zero_handover['Ncell_lat'] = df_zero_handover['Ncell'].map(lambda x:lonlat_dict.get(x, default=('',''))[1])

neighbor_dict = {cell:df_cur_config['Ncell'][df_cur_config['Scell'] == cell].to_list() for cell in tqdm(set(df_cur_config['Scell']))}

# 保存邻区字典
with open('neighbor_dict.txt','w') as f:
    f.write(str(neighbor_dict))

# 读取邻区字典
with open('neighbor_dict.txt','r') as f:
    neighbor_dict = eval(f.read())

