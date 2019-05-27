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
     xy_coordinate.append(int(round(x)))
     xy_coordinate.append(int(round(y)))
     return xy_coordinate # 装换后的 x,y 坐标

def lon2x(lon):
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
     return round(x)

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
     return round(y)


df_cell = pd.read_csv(data_path + cell_file,engine = 'python' )
df_cell.drop_duplicates('eNodeB_ID', keep='first', inplace = True)
df_cell['xy_coordinate'] = df_cell.apply(lambda x:millerToXY(x.LON , x.LAT) , axis = 1 )
df_cell['x坐标'] = df_cell['LON'].map(lambda x:lon2x(x))
df_cell['y坐标'] = df_cell['LAT'].map(lambda x:lon2x(x))
df_cell['merdge_index'] = df_cell['x坐标'].map(str) + '_' + df_cell['y坐标'].map(str)
df_cell = df_cell.reset_index()
df_cell.drop('index',axis =0,inplace = True)
# 初始化种子点
point_list = [x for x in df_cell['xy_coordinate']]
points = np.array(point_list)
# 计算Voronoi图
vor = Voronoi(points=points)

seed_ponts = vor.points
df_voronoi = pd.DataFrame(seed_points,columns=['x坐标','y坐标'])
df_voronoi['merdge_index'] = df_voronoi['x坐标'].map(int).map(str) + '_' + df_cell['y坐标'].map(int).map(str)
df_cell_info = df_cell[['merdge_index','eNodeB_ID','Cell_name']]

df_voronoi = pd.merge(df_voronoi ,df_cell_info,how = 'left' , on = 'merdge_index' )
df_voronoi['']
point_region = vor.point_region
regions = vor.regions

points[0]
regions[3228]

ridge_vertices =vor.ridge_vertices
ridge_points = vor.ridge_points
ridge_points[6554]

#     max_bound: 种子点的最大边界
#     min_bound: 种子点的最小边界
#     ndim: 种子点维度
#     npoints: 种子点数量
#     point_region: 种子点所对应的区域index
#     points: 种子点
#     regions: Voronoi区域
#     ridge_dict: 分界线字典
#     ridge_points: 分界线段
#     ridge_vertices:
#     vertices: 多边形分界线的交点，顶点