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
zte_bts800 = '曲靖电信LTE工参(L800M)20190425.xls'
zte_bts1800 = '曲靖电信LTE工参(L1.8G)20190425.xls'
zte_eric800 ='爱立信云南曲靖电信工参表20190428.xlsx'
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

df_tmp = pd.read_excel(data_path + zte_bts800)
df_zte800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_zte800['eNodeB_ID'] = df_tmp['ENODEBID']
df_zte800['Cell_name'] = df_tmp['CELLNAME']
name = df_tmp['ENODEBID'].map(str)  + '_' + df_tmp['CELLNAME'].map(lambda x:x.split('_')[2])
df_zte800['name'] = name
df_zte800['Cell_index'] = df_tmp['ENODEBID'].map(str)  + df_tmp['CELLID'].map(str)
df_zte800['LON'] = df_tmp['LONC']
df_zte800['LAT'] = df_tmp['LATC']
df_zte800['azimuth'] = df_tmp['Azimuth']
df_zte800['network'] = 'L800'
df_zte800['manufacturers'] = 'ZTE'

df_tmp = pd.read_excel(data_path + zte_bts1800)
df_zte1800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_zte1800['eNodeB_ID'] = df_tmp['ENODEBID']
df_zte1800['Cell_name'] = df_tmp['CELLNAME']
df_zte1800['name'] = df_tmp['CELLNAME'].map(lambda x:x.split('_')[2])
name = df_tmp['ENODEBID'].map(str)  + '_' + df_tmp['CELLNAME'].map(lambda x:x.split('_')[2])
df_zte1800['name'] = name
df_zte1800['Cell_index'] = df_tmp['ENODEBID'].map(str)  + df_tmp['CELLID'].map(str)
df_zte1800['LON'] = df_tmp['LONC']
df_zte1800['LAT'] = df_tmp['LATC']
df_zte1800['azimuth'] = df_tmp['Azimuth']
df_zte1800['network'] = 'L1.8'
df_zte1800['manufacturers'] = 'ZTE'

df_tmp = pd.read_excel(data_path + zte_eric800)
df_eric800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_eric800['eNodeB_ID'] = df_tmp['eNBId']
df_eric800['Cell_name'] = df_tmp['Cell_name']
name = df_tmp['eNBId'].map(str)  + '_' + df_tmp['Cell_name'].map(lambda x:x.split('_')[0])
df_eric800['name'] = name
df_eric800['Cell_index'] =  df_tmp['Cell_index']
df_eric800['LON'] = df_tmp['longitude']
df_eric800['LAT'] = df_tmp['latitude']
df_eric800['azimuth'] = df_tmp['azimuth']
df_eric800['network'] = df_tmp['channelBandwidth'].map({'5M':'L800M', '15M':'L1.8'})
df_eric800['manufacturers'] = 'ERIC'

df_all_cells = df_zte800.append(df_zte1800).append(df_eric800)
df_all_cells = df_all_cells.reset_index()
df_all_cells.drop('index',axis =1,inplace =True)
with open(data_path + '全网小区汇总.csv','w') as  writer:
     df_all_cells.to_csv(writer,index = False)


# =============================================================================
# 规划
# =============================================================================
#df_all_cells = pd.read_csv(data_path + 'test.csv',engine = 'python')
df_cell = df_all_cells.drop_duplicates('name', keep='first')
df_cell = df_cell[~df_cell['Cell_name'].str.contains('室分') ]
df_cell['xy_coordinate'] = df_cell.apply(lambda x:millerToXY(x.LON , x.LAT) , axis = 1 )
df_cell = df_cell.reset_index()
df_cell.drop('index',axis =1,inplace = True)

# 初始化种子点
point_list = [x for x in df_cell['xy_coordinate']]
points = np.array(point_list)
# 计算Voronoi图
vor = Voronoi(points=points)
voronoi_plot_2d(vor)
plt.show()

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
layer1_neighbor_name_dict = dict()
layer1_regions_dict = dict()
for i in range(10):
     neighbors_name_layer1 = []
     neighbors_index_layer1 = []
     regions_layer1 = []
     cell_name = df_cell.loc[i,'name']
     cell_index = df_cell.loc[i,'Cell_index']
     cell_region = df_cell.loc[i,'regions']
     for j in range(0,len(df_cell)):
          if len(set(cell_region) & set(df_cell.loc[j,'regions'])) > 0 \
               and df_cell.loc[j,'name'] != cell_name:
                    neighbors_name_layer1.append(df_cell.loc[j,'name'])
                    regions_layer1.append(df_cell.loc[j,'regions'])
     layer1_neighbor_name_dict[cell_name]= neighbors_name_layer1
     layer1_regions_dict[cell_index] = regions_layer1

# =============================================================================
# 规划第二层邻区
# =============================================================================
layer2_neighbor_name_dict = dict()
for i in range(10):
     neighbors_name_layer2 = []
     cell_name = df_cell.loc[i,'name']
     cell_index = df_cell.loc[i,'Cell_index']
     for layer1_region in layer1_regions_dict[cell_index]:
          for j in range(0,len(df_cell)):
               if len(set(layer1_region) & set(df_cell.loc[j,'regions'])) > 0 \
                    and df_cell.loc[j,'regions'] not in layer1_regions_dict[cell_index]\
                    and df_cell.loc[j,'regions'] != df_cell.loc[i,'regions']:
                         neighbors_name_layer2.append(df_cell.loc[j,'name'])
     layer2_neighbor_name_dict[cell_name]= list(set(neighbors_name_layer2))

df_cell['layer1_neighbor'] = df_cell['name'].map(layer1_neighbor_name_dict)
df_cell['layer2_neighbor'] = df_cell['name'].map(layer2_neighbor_name_dict)

with open(data_path + '全网layer规划.xlsx','w') as  writer:
     df_cell.to_csv(writer,index = False)

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