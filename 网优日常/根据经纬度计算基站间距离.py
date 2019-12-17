# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:30:48 2019

@author: Administrator
"""

import os
import pandas as pd
from tqdm import tqdm,trange
import time
from datetime import datetime
from math import sin
from math import cos
from math import tan
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
from math import ceil


def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    # 如果源小区和目标小区经纬度相同，会出现除于0的情况报错，所以要确保经纬度不同再开始计算
    if latA != latB and lonA != lonB:
        pA = atan(rb / ra * tan(radLatA))
        pB = atan(rb / ra * tan(radLatB))
        x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
        c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
        c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (x + dr)
        return distance
    else:
        return 0


data_path = 'D:/_python小程序/根据经纬度计算基站间距离'
os.chdir(data_path)

source_cell_info = 'source_bts_info.xlsx'
destination_cell_info = 'destination_bts_info.xlsx'

max_distance = 2000

df_source_cell = pd.read_excel(source_cell_info)
df_source_cell['lon'] = df_source_cell['lon'].map(lambda x: round(x, 5))
df_source_cell['lat'] = df_source_cell['lat'].map(lambda x: round(x, 5))

df_destination_cell = pd.read_excel(destination_cell_info)
df_destination_cell['lon'] = df_destination_cell['lon'].map(lambda x: round(x, 5))
df_destination_cell['lat'] = df_destination_cell['lat'].map(lambda x: round(x, 5))
df_destination_cell.rename(
    columns={
        'name': 'des_name',
        'eNodeB': 'des_eNodeB',
        'lon': 'des_lon',
        'lat': 'des_lat'},
    inplace=True)

list_res = []
start_time = datetime.now()

with tqdm(total=len(df_source_cell)) as t:
    for i in range(len(df_source_cell)):
        t.update(1)
        df_tmp = df_destination_cell
        df_tmp['s_name'] = df_source_cell.loc[i, 'name']
        df_tmp['s_eNodeB'] = df_source_cell.loc[i, 'eNodeB']
        df_tmp['s_lon'] = df_source_cell.loc[i, 'lon']
        df_tmp['s_lat'] = df_source_cell.loc[i, 'lat']
        df_tmp['distance'] = df_tmp.apply(
            lambda x: getDistance(
                x.s_lat,
                x.s_lon,
                x.des_lat,
                x.des_lon),
            axis=1)
        df_tmp = df_tmp[df_tmp['distance'] <= max_distance]
        list_res.append(df_tmp)
        if i == len(df_source_cell) - 1:
            total_time = datetime.now()
            delta_time = (total_time - start_time).seconds
            print('\n', '  Global Report  '.center(60, '#'))
            print('ALL {total} cells finished !'.format(total=len(df_source_cell)))
            print('Total take {seconds} seconds!'.format(seconds=delta_time))

df_res = pd.concat(list_res, axis=0)
df_res = df_res[['s_name', 's_eNodeB', 's_lon', 's_lat', 'des_name',
                 'des_eNodeB', 'des_lon', 'des_lat', 'distance']]
df_res['distance'] = df_res['distance'].map(lambda x: ceil(x))
with open('距离计算结果.csv', 'w') as writer:
    df_res.to_csv(writer, index=False)
print('\n' + '结果已输出到：{path}，请到该目录查看！'.format(path=os.getcwd().replace('\\\\', '\\') + '\\'))
os.startfile(data_path)
