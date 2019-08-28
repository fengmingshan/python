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

data_path ='D:/_小程序/新开站邻区规划/'
cell_file = '西城规划扇区.xlsx'

def millerToXY (lon, lat):
     xy_coordinate = [] # x，y坐标集
     '''
     经纬度转换为平面坐标系中的x,y 利用米勒坐标系
     :param lon: 经度
     :param lat: 维度
     '''
     L = 6381372*math.pi*2
     W = L
     H = L/2
     mill = 2.3
     x = lon*math.pi/180
     y = lat*math.pi/180
     y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
     x = (W/2)+(W/(2*math.pi))*x
     y = (H/2)-(H/(2*mill))*y
     xy_coordinate.append(int(round(x,8)))
     xy_coordinate.append(int(round(y,8)))
     return xy_coordinate # 装换后的 x,y 坐标

df_cell = pd.read_excel(data_path + cell_file)

df_bts = df_cell[['ENODEBName','LONB','LATB']]
df_bts.drop_duplicates('ENODEBName',keep = 'first',inplace = True)
df_bts['xy_coordinate'] = df_bts.apply(lambda x:millerToXY(x.LONB , x.LATB) , axis = 1 )
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
df_bts = pd.merge(df_bts,df_regions,on = 'regions_index',how = 'left' )

df_bts_regions = df_bts[['ENODEBName','regions']]
df_bts_regions.set_index('ENODEBName',inplace = True)
dict_regions = df_bts_regions.to_dict()

df_cell['regions'] = df_cell['ENODEBName'].map(dict_regions)

plan_bts_name = '麒麟西城师范学院樱苑二栋L8'
df_cell = df_cell[df_cell['ENODEBName'] != plan_bts_name]
# =============================================================================
# 规划第一层邻区
# =============================================================================
def plan_first_layer(plan_bts_name,df_bts):
    df_bts = df_bts[df_bts['ENODEBName'] != plan_bts_name]
    layer1_neighbor_name_dict = dict()
    layer1_regions_dict = dict()

        cell_name = df_cell.loc[i,'name']
        cell_index = df_cell.loc[i,'Cell_index']
        cell_region = df_cell.loc[i,'regions']
    for j in range(0,len(df_bts)):
        if len(set(cell_region) & set(df_cell.loc[j,'regions'])) > 0 \
            and df_cell.loc[j,'name'] != cell_name:
                neighbors_name_layer1.append(df_cell.loc[j,'name'])
                regions_layer1.append(df_cell.loc[j,'regions'])
     layer1_neighbor_name_dict[cell_name]= neighbors_name_layer1
     layer1_regions_dict[cell_index] = regions_layer1
