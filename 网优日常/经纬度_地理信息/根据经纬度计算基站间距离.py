# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:30:48 2019

@author: Administrator
"""

import os
import pandas as pd
from tqdm import tqdm,trange
from datetime import datetime
from math import sin
from math import cos
from math import tan
from math import asin
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
from math import sqrt
from math import ceil


def calc_Distance(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)]) # 经纬度转换成弧度
    dlon = lon2-lon1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance,0)
    return distance


data_path = 'D:/_python小程序/根据经纬度计算基站间距离'
os.chdir(data_path)

source_cell_info = '铁塔站址.xlsx'
destination_cell_info = '铁塔站址.xlsx'

min_distance = 300


df_source_cell = pd.read_excel(source_cell_info)
df_source_cell.columns=['name','eNodeB','lon','lat']
df_source_cell = df_source_cell[df_source_cell['lon']!='——']

df_source_cell['lon'] = df_source_cell['lon'].astype(float)
df_source_cell['lat'] = df_source_cell['lat'].astype(float)
df_source_cell['lon'] = df_source_cell['lon'].map(lambda x: round(x, 5))
df_source_cell['lat'] = df_source_cell['lat'].map(lambda x: round(x, 5))

df_destination_cell = pd.read_excel(destination_cell_info)
df_destination_cell.columns=['name','eNodeB','lon','lat']
df_destination_cell = df_destination_cell[df_destination_cell['lon']!='——']

df_destination_cell['lon'] = df_destination_cell['lon'].astype(float)
df_destination_cell['lat'] = df_destination_cell['lat'].astype(float)

df_destination_cell['lon'] = df_destination_cell['lon'].map(lambda x: round(x, 5))
df_destination_cell['lat'] = df_destination_cell['lat'].map(lambda x: round(x, 5))
df_destination_cell['lon'] = df_destination_cell['lon'].map(lambda x: round(x, 5))
df_destination_cell['lat'] = df_destination_cell['lat'].map(lambda x: round(x, 5))

df_res = pd.DataFrame()
df_res['s_eNodeB'] = tqdm([x for x in df_source_cell['eNodeB'] for y in df_destination_cell['eNodeB']])
df_res['s_name'] = tqdm([x for x in df_source_cell['name'] for y in df_destination_cell['name']])
df_res['s_lon'] = tqdm([x for x in df_source_cell['lon'] for y in df_destination_cell['lon']])
df_res['s_lat'] = tqdm([x for x in df_source_cell['lat'] for y in df_destination_cell['lat']])
df_res['des_eNodeB'] = tqdm([y for x in df_source_cell['eNodeB'] for y in df_destination_cell['eNodeB']])
df_res['des_name'] = tqdm([y for x in df_source_cell['name'] for y in df_destination_cell['name']])
df_res['des_lon'] = tqdm([y for x in df_source_cell['lon'] for y in df_destination_cell['lon']])
df_res['des_lat'] = tqdm([y for x in df_source_cell['lat'] for y in df_destination_cell['lat']])
df_res['distance'] = tqdm([calc_Distance(a, b, c, d) for a, b, c, d in zip(
df_res['s_lon'], df_res['s_lat'], df_res['des_lon'], df_res['des_lat'])])

df_res = df_res[['s_name', 's_eNodeB', 's_lon', 's_lat', 'des_name', 'des_eNodeB', 'des_lon', 'des_lat', 'distance']]
df_res['distance'] = df_res['distance'].map(lambda x: ceil(x))

df_min_distance = df_res[(df_res['distance'] <= 300)&(df_res['s_eNodeB'] != df_res['des_eNodeB'])]
with open('最小距离.csv', 'w', newline = '') as writer:
    df_min_distance.to_csv(writer, index=False)

with open('全量表格.csv', 'w', newline = '') as writer:
    df_res.to_csv(writer, index=False)

print('\n' + '结果已输出到：{path}，请到该目录查看！'.format(path=os.getcwd().replace('\\\\', '\\') + '\\'))
os.startfile(data_path)
