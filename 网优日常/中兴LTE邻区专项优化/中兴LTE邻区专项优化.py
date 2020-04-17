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

df_cur_config = pd.read_excel('./全网已配置邻区_简.xlsx',enging ='python')
df_cur_config['Scell'] =df_cur_config['MEID'].map(str) + '_' + df_cur_config['CellId'].map(str)
df_cur_config['Ncell'] =df_cur_config['eNBId'].map(str) + '_' + df_cur_config['NCellId'].map(str)
df_cur_config['ralations'] =df_cur_config['Scell'] + '-' + df_cur_config['Ncell']

df_zero_handover = df_cur_config[['Scell','Ncell','ralations']][~df_cur_config['ralations'].isin(df['ralations'])]

neighbor_dict = tqdm({cell:list(df_cur_config['Ncell'][df_cur_config['Scell'] = cell]) for cell in set(df_cur_config['Scell'])})