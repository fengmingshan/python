# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 14:34:08 2018

@author: Administrator
"""
import pandas as pd
import geopy.distance

data_path = r'D:\test' + '\\'
file = '曲靖CELL.xlsx'

def get_distance_point(lat, lon, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：270）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = geopy.distance.VincentyDistance(meters=distance)
    return d.destination(point=start, bearing=direction)

df_cell = pd.read_excel(data_path + file ,encoding = 'utf-8' )
df_cell['CELL_LON'] = ''
df_cell['CELL_LAT'] = ''
for i in range(0,len(df_cell),1):
    p = get_distance_point( df_cell.loc[i,'LAT'], df_cell.loc[i,'LON'], 250, df_cell.loc[i,'方位角'])
    df_cell.loc[i,'CELL_LON'] = round(p.longitude,6)
    df_cell.loc[i,'CELL_LAT'] = round(p.latitude,6)

with pd.ExcelWriter(data_path  + '曲靖市_全市扇区数据清单(无线中心).xlsx') as writer:
    df_cell.to_excel(writer,'全市扇区数据清单',index= False) 

