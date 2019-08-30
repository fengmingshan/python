# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:32:43 2019

@author: Administrator
"""
import pandas as pd
import os
import math
import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
from numba import jit
from functools import reduce
import operator

from math import sin
from math import cos
from math import tan
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
from math import ceil

data_path = 'D:/_小程序/新开站邻区规划/'
cell_file = '西城规划扇区.xlsx'


def millerToXY(lon, lat):
    xy_coordinate = []  # x，y坐标集
    '''
     经纬度转换为平面坐标系中的x,y 利用米勒坐标系
     :param lon: 经度
     :param lat: 维度
     '''
    L = 6381372 * math.pi * 2
    W = L
    H = L / 2
    mill = 2.3
    x = lon * math.pi / 180
    y = lat * math.pi / 180
    y = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y))
    x = (W / 2) + (W / (2 * math.pi)) * x
    y = (H / 2) - (H / (2 * mill)) * y
    xy_coordinate.append(int(round(x, 8)))
    xy_coordinate.append(int(round(y, 8)))
    return xy_coordinate  # 装换后的 x,y 坐标


def clac_degree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng


def calc_azimuth_difference(Degree, Scell_azimuth, Ncell_azimuth):
    '''计算目标小区是否要添加为邻区
       根据距离和方位角判断：
       当基站距离小于2km时，源小区和目标基站所有小区都要添加为邻区;
       当基站距离大于2km小于5km时，只有源小区正对目标小区的扇区和目标基站所有小区添加邻区;
       当基站距离大于5km时，只有源小区正对目标小区的扇区和目标基站正对源小区的小区添加邻区;'''
    Scell_degree_detal = abs(Scell_azimuth - Degree) if abs(Scell_azimuth - Degree) < 180 \
        else 360 - abs(Scell_azimuth - Degree)
    neighbor_Degree_detal = abs(Ncell_azimuth - Degree) if abs(Ncell_azimuth - Degree) < 180 \
        else 360 - abs(Ncell_azimuth - Degree)
    if Scell_degree_detal + neighbor_Degree_detal <= 90:
        add_neighbor = 'Yes'
    else:
        add_neighbor = 'No'
    return add_neighbor


df_cell = pd.read_excel(data_path + cell_file)

df_bts = df_cell[['ENODEBName', 'LONB', 'LATB']]
df_bts.drop_duplicates('ENODEBName', keep='first', inplace=True)
df_bts['xy_coordinate'] = df_bts.apply(
    lambda x: millerToXY(x.LONB, x.LATB), axis=1)
# 初始化种子点
point_list = [x for x in df_bts['xy_coordinate']]
points = np.array(point_list)
# 计算Voronoi图
vor = Voronoi(points=points)
voronoi_plot_2d(vor)
plt.show()

# 获取种子点的index
df_bts['point_index'] = list(df_bts.index)

# 获取种子点的region_index
point_region = vor.point_region
df_bts['regions_index'] = point_region

# 获取regions的详细信息
regions = vor.regions
df_regions = pd.DataFrame()
df_regions['regions_index'] = range(len(regions))
df_regions['regions'] = regions
df_bts = pd.merge(df_bts, df_regions, on='regions_index', how='left')

df_bts_regions = df_bts[['ENODEBName', 'regions']]
df_bts_regions.set_index('ENODEBName', inplace=True)
dict_regions = df_bts_regions['regions'].to_dict()
df_cell['regions'] = df_cell['ENODEBName'].map(dict_regions)
plan_bts_name = '麒麟西城师范学院樱苑二栋L8'

# =============================================================================
# 规划邻区
# =============================================================================
@jit 
def plan_first_layer(plan_bts_name, df_cell):
    df_cell['Scell'] = ''
    df_cell['first_layer'] = ''
    df_cell['second_layer'] = ''
    df_cell['degree'] = ''
    df_cell['opposite'] = ''
    df_plan_cell = df_cell[df_cell['ENODEBName'] == plan_bts_name]
    plan_cell = list(set(df_plan_cell['CELLNAME']))
    cell_region = set(list(df_plan_cell['regions'])[0])
    for i in range(0, len(df_cell)):
        if len(cell_region & set(df_cell.loc[i, 'regions'])) > 0 \
                and df_cell.loc[i, 'CELLNAME'] != plan_cell:
            df_cell.loc[i, 'first_layer'] = 1
    # 筛选出第一层邻区清单
    df_first_layer = df_cell[df_cell['first_layer'] == 1]
    df_first = pd.DataFrame()
    for i in range(0, len(plan_cell)):
        if len(plan_cell) - 1 - i >= 0:
            df_tmp = df_first_layer.copy()
            df_tmp['Scell'] = plan_cell[len(plan_cell) - i - 1]
            df_first = df_first.append(df_tmp, ignore_index=True)

    # 计算第一层邻区及第一层邻区的regions
    first_layer_neighbor = list(df_first_layer['CELLNAME'])
    first_layer_regions = set(
        reduce(operator.concat, list(df_first_layer['regions'])))
    S_Lon = list(df_plan_cell['LONB'])[0]
    S_Lat = list(df_plan_cell['LATB'])[0]
    S_Azimuth = list(df_plan_cell['Azimuth'])[0]
    df_second = pd.DataFrame()
    for cell in plan_cell:
        for i in range(0, len(df_cell)):
            if len(first_layer_regions & set(df_cell.loc[i, 'regions'])) > 0 \
                    and df_cell.loc[i, 'CELLNAME'] != cell \
                    and df_cell.loc[i, 'CELLNAME'] not in first_layer_neighbor:
                df_cell.loc[i, 'second_layer'] = 1
                df_cell.loc[i, 'Scell'] = cell
                df_cell.loc[i, 'degree'] = clac_degree(
                    S_Lon, S_Lat, df_cell.loc[i, 'LONB'], df_cell.loc[i, 'LATB'])
                df_cell['opposite'] = calc_azimuth_difference(
                    df_cell.loc[i, 'degree'], S_Azimuth, df_cell.loc[i, 'Azimuth'])
            else:
                df_cell.loc[i, 'second_layer'] = 0
            df_second_layer = df_cell[(df_cell['second_layer'] == 1) & (
                df_cell['opposite'] == 'Yes')]
            df_second = df_second.append(df_second_layer)
    df_planed = df_first.append(df_second, ignore_index=True)
    return df_planed


df_planed = plan_first_layer('麒麟西城师范学院樱苑二栋L8', df_cell)
df_planed = df_planed[['Scell', 'CELLNAME', 'first_layer', 'second_layer']]
df_planed.rename(columns={'CELLNAME': 'Ncell'}, inplace=True)
df_planed.drop_duplicates(['Scell', 'Ncell'], keep='first', inplace=True)
with pd.ExcelWriter(data_path + '邻区规划结果.xlsx') as writer:
    df_planed.to_excel(writer, index=False)
