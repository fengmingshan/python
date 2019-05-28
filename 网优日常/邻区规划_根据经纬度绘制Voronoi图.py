# -*- coding: utf-8 -*-
"""
Created on Mon May 27 08:45:59 2019

@author: Administrator
"""

import pandas as pd
import os
import math
import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt

data_path ='D:\_邻区自动规划' + '\\'
cell_file = '全网小区_合并.csv'

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

def lon2x(lon)
     '''
     经度转换为平面坐标系中的x 利用米勒坐标系
     :param lon: 经度
     '''
     L = 6381372*math.pi*2
     W = L
     H = L/2
     mill = 2.3
     x = lon*math.pi/180
     x = (W/2)+(W/(2*math.pi))*x
     return round(x,5)

def lat2y (lat):
     '''
     纬度转换为平面坐标系中的y 利用米勒坐标系
     :param lat: 维度
     '''
     L = 6381372*math.pi*2
     W = L
     H = L/2
     mill = 2.3
     y = lat*math.pi/180
     y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
     y = (H/2)-(H/(2*mill))*y
     return round(y,5)


df_cell = pd.read_csv(data_path + cell_file,engine = 'python' )
df_cell.drop_duplicates('eNodeB_ID', keep='first', inplace = True)
df_cell['xy_coordinate'] = df_cell.apply(lambda x:millerToXY(x.LON , x.LAT) , axis = 1 )
df_cell = df_cell.reset_index()
df_cell.drop('index',axis =1,inplace = True)
# 初始化种子点
point_list = [x for x in df_cell['xy_coordinate']]
points = np.array(point_list)
# 计算Voronoi图
vor = Voronoi(points=points)

seed_ponts = vor.points
df_cell['point_index'] = list(df_cell.index)

point_region = vor.point_region
df_cell['regions_index'] = point_region

regions = vor.regions
df_regions = pd.DataFrame()
df_regions['regions_index'] = range(len(regions))
df_regions['regions'] = regions
df_cell = pd.merge(df_cell,df_regions,on = 'regions_index',how = 'left' )


# =============================================================================
# 规划第一层邻区
# =============================================================================
layer1_neighbor_dict = dict()
layer1_regions_dict = dict()
for i in range(3):
     neighbors_layer1 = []
     regions_layer1 = []
     cell_name = df_cell.loc[i,'Cell_name']
     cell_region = df_cell.loc[i,'regions']
     for j in range(0,len(df_cell)):
          if len(set(cell_region) & set(df_cell.loc[j,'regions'])) > 0 \
               and df_cell.loc[j,'regions'] != cell_region:
                    neighbors_layer1.append(df_cell.loc[j,'Cell_name'])
                    regions_layer1.append(df_cell.loc[j,'regions'])
     layer1_neighbor_dict[cells_name]= neighbors_layer1
     layer1_regions_dict[cells_region] = regions_layer1

# =============================================================================
# 规划第二层邻区
# =============================================================================
layer2_neighbor_dict = dict()
layer2_regions_dict = dict()
for i in range(3):
     cell_name = df_cell.loc[i,'Cell_name']
     cell_region = df_cell.loc[i,'regions']
     neighbors_layer_2 = []
     regions_layer_2 = []
     for layer1_region in layer1_regions_dict[cell_region]:
          for j in range(0,len(df_cell)):
               if len(set(layer1_region) & set(df_cell.loc[j,'regions'])) > 0 \
                    and df_cell.loc[j,'regions'] != layer1_region:
                         neighbors_layer_2.append(df_cell.loc[j,'Cell_name'])
                         regions_layer_2.append(df_cell.loc[j,'regions'])
     layer2_neighbor_dict[cells_name]= neighbors_layer_2
     layer2_regions_dict[cells_region] = regions_layer_2


# max_bound: 种子点的最大边界
# min_bound: 种子点的最小边界
# ndim: 种子点维度
# npoints: 种子点数量
# point_region: 种子点所对应的区域index
# points:  种子点,seed_point,2列的数组
# regions: Voronoi区域,一个regions对应多个 vertices_index,-1表示顶点在无限远
# ridge_dict: 分界线字典
# ridge_points: 每条Voronoi分界线两侧的两个种子点seed_point的index
# ridge_vertices:regions每条边的端点的index，每一个ridge_vertices_index对应两个vertices的index,-1表示端点在无限远处
# vertices: regions多边形的顶点坐标，2列的数组