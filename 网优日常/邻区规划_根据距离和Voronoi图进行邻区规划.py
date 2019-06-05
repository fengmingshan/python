# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:09:12 2019

@author: Administrator
"""
import os
import pandas as pd
import numpy as np
from scipy.spatial import Voronoi
import time
from datetime import datetime
import math
from math import sin
from math import cos
from math import tan
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
from math import ceil

L800_max_distance = 10000
L1800_max_distance = 2000
mix_max_distance = 5000

L1800_neighbor_layer = 2
L800_neighbor_layer = 1
mix_neighbor_layer = 1

data_path = r'd:\_邻区自动规划' + '\\'
cell_info = '全网小区.csv'

def getDegree(latA, lonA, latB, lonB):
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

def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance

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

def plan_neighbor_bts(df_bts):
     df_bts['xy_coordinate'] = df_bts.apply(lambda x:millerToXY(x.N_LON , x.N_LAT) , axis = 1 )
     # 初始化种子点
     point_list = [x for x in df_bts['xy_coordinate']]
     if len(point_list) >=4:
         points = np.array(point_list)
         # 计算Voronoi图
         vor = Voronoi(points=points)
    
         seed_ponts = vor.points
         df_bts['point_index'] = list(df_bts.index)
    
         point_region = vor.point_region
         df_bts['regions_index'] = point_region
    
         regions = vor.regions
         df_regions = pd.DataFrame()
         df_regions['regions_index'] = range(len(regions))
         df_regions['regions'] = regions
         df_bts = pd.merge(df_bts,df_regions,on = 'regions_index',how = 'left' )
         # =============================================================================
         # 规划第一层邻区
         # =============================================================================
         layer1_neighbor_name_dict = dict()
         layer1_regions_dict = dict()
         for i in range(len(df_bts)):
              neighbors_name_layer1 = []
              neighbors_index_layer1 = []
              regions_layer1 = []
              cell_name = df_bts.loc[i,'N_bts_name']
              cell_region = df_bts.loc[i,'regions']
              for j in range(0,len(df_bts)):
                   if len(set(cell_region) & set(df_bts.loc[j,'regions'])) > 0 \
                        and df_bts.loc[j,'N_bts_name'] != cell_name:
                        neighbors_name_layer1.append(df_bts.loc[j,'N_bts_name'])
                        regions_layer1.append(df_bts.loc[j,'regions'])
              layer1_neighbor_name_dict[cell_name]= neighbors_name_layer1
              layer1_regions_dict[cell_name] = regions_layer1
         # =============================================================================
         # 规划第二层邻区
         # =============================================================================
         layer2_neighbor_name_dict = dict()
         for i in range(len(df_bts)):
              neighbors_name_layer2 = []
              cell_name = df_bts.loc[i,'N_bts_name']
              for layer1_region in layer1_regions_dict[cell_name]:
                   for j in range(0,len(df_bts)):
                        if len(set(layer1_region) & set(df_bts.loc[j,'regions'])) > 0 \
                             and df_bts.loc[j,'regions'] not in layer1_regions_dict[cell_name]\
                             and df_bts.loc[j,'regions'] != df_bts.loc[i,'regions']:
                             neighbors_name_layer2.append(df_bts.loc[j,'N_bts_name'])
              layer2_neighbor_name_dict[cell_name]= list(set(neighbors_name_layer2))
         df_bts['layer1_neighbor'] = df_bts['S_bts_name'].map(layer1_neighbor_name_dict)
         df_bts['layer2_neighbor'] = df_bts['S_bts_name'].map(layer2_neighbor_name_dict)
     elif len(point_list) <4:
         df_bts['layer1_neighbor'] = list(df_bts['N_bts_name'])
         df_bts['layer2_neighbor'] = list(df_bts['N_bts_name'])     
     return df_bts

def plan_neighbor_cell(Degree,Scell_azimuth,Ncell_azimuth):
     '''计算目标小区是否要添加为邻区
        根据距离和方位角判断：
        当基站距离小于2km时，源小区和目标基站所有小区都要添加为邻区;
        当基站距离大于2km小于5km时，只有源小区正对目标小区的扇区和目标基站所有小区添加邻区;
        当基站距离大于5km时，只有源小区正对目标小区的扇区和目标基站正对源小区的小区添加邻区;'''
     Degree_detal = abs(Scell_azimuth - Degree) if abs(Scell_azimuth - Degree) < 180 \
                    else 360 - abs(Scell_azimuth - Degree)
     neighbor_Degree_detal = abs(Ncell_azimuth - Degree) if abs(Ncell_azimuth - Degree) < 180 \
                              else 360 - abs(Ncell_azimuth - Degree)
     if Degree_detal< 60 and neighbor_Degree_detal < 60:
          add_neighbor ='Yes'
     else:
          add_neighbor ='No'
     return add_neighbor

df_cell_info = pd.read_csv(data_path + cell_info, engine = 'python' )
df_cell_info = df_cell_info[~df_cell_info['Cell_name'].str.contains('室分')]
df_bts =  df_cell_info.drop_duplicates('name' ,keep = 'first')
df_bts = df_bts[['name','network','LON','LAT']]
df_bts = df_bts.reset_index().drop('index',axis =1)

# =============================================================================
# 开始规划邻区
# =============================================================================
print('开始规划邻区，共',len(df_bts),'个基站需要规划！')
plan_result = []
start_time = time.time()
#for i in range(len(df_bts)):
for i in range(801,len(df_bts)):
     df_tmp = pd.DataFrame(index = range(len(df_bts)))
     df_tmp['S_bts_name'] = df_bts.loc[i,'name']
     df_tmp['S_LON'] = df_bts.loc[i,'LON']
     df_tmp['S_LAT'] = df_bts.loc[i,'LAT']
     df_tmp['S_network'] = df_bts.loc[i,'network']
     df_tmp['N_bts_name'] = df_bts['name']
     df_tmp['N_LON'] = df_bts['LON']
     df_tmp['N_LAT'] = df_bts['LAT']
     df_tmp['N_network'] = df_bts['network']
     df_tmp['Degree'] = df_tmp.apply(lambda x :getDegree(x.S_LAT,x.S_LON,x.N_LAT,x.N_LON)\
           if (x.S_LAT != x.N_LAT) and (x.S_LON != x.N_LON) else 0,axis =1)
     df_tmp['Distance'] = df_tmp.apply(lambda x :getDistance(x.S_LAT,x.S_LON,x.N_LAT,x.N_LON)\
           if (x.S_LAT != x.N_LAT) and (x.S_LON != x.N_LON) else 0,axis =1)
     df_tmp['relation'] = df_tmp['S_bts_name'] + '_' + df_tmp['N_bts_name']

     df_Degree = df_tmp[['relation','Degree']].set_index('relation')
     Degree_dict = df_Degree.to_dict()['Degree']
# =============================================================================
# 根据距离和网络类型筛选相邻的bts，并进行plan_neighbor
# =============================================================================
     if df_bts.loc[i,'network'] == 'L1.8':
          df_neighbor_bts1 = df_tmp[(df_tmp['N_network'] == 'L1.8')&(df_tmp['Distance'] <= L1800_max_distance)]
          df_neighbor_bts1 = plan_neighbor_bts(df_neighbor_bts1)
          df_neighbor_bts1 = df_neighbor_bts1.reset_index().drop('index',axis = 1)

          df_neighbor_bts2 = df_tmp[((df_tmp['N_bts_name'] == df_bts.loc[i,'name'])|(df_tmp['N_network'] == 'L800'))
                                        &(df_tmp['Distance'] <= mix_max_distance)]
          df_neighbor_bts2 = plan_neighbor_bts(df_neighbor_bts2)
          df_neighbor_bts2 = df_neighbor_bts2.reset_index().drop('index',axis = 1)

          layer1_neighbor_bts = []
          layer2_neighbor_bts = []
          if isinstance(df_neighbor_bts1.loc[0,'layer1_neighbor'],list) :
              layer1_neighbor_bts.extend(df_neighbor_bts1.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.extend(df_neighbor_bts1.loc[0,'layer2_neighbor'])
          else:
              layer1_neighbor_bts.append(df_neighbor_bts1.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.append(df_neighbor_bts1.loc[0,'layer2_neighbor'])
              
          if isinstance(df_neighbor_bts2.loc[0,'layer1_neighbor'],list):
              layer1_neighbor_bts.extend(df_neighbor_bts2.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.extend(df_neighbor_bts2.loc[0,'layer2_neighbor'])
          else:
              layer1_neighbor_bts.append(df_neighbor_bts2.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.append(df_neighbor_bts2.loc[0,'layer2_neighbor'])


     elif df_bts.loc[i,'network'] == 'L800':
          df_neighbor_bts1 = df_tmp[((df_tmp['N_bts_name'] == df_bts.loc[i,'name'])|(df_tmp['N_network'] == 'L1.8'))
                                        &(df_tmp['Distance'] <= mix_max_distance)]
          df_neighbor_bts1 = plan_neighbor_bts(df_neighbor_bts1)
          df_neighbor_bts1 = df_neighbor_bts1.reset_index().drop('index',axis = 1)
          
          df_neighbor_bts2 = df_tmp[(df_tmp['N_network'] == 'L800')&(df_tmp['Distance'] <= L800_max_distance)]
          df_neighbor_bts2 = plan_neighbor_bts(df_neighbor_bts2)
          df_neighbor_bts2 = df_neighbor_bts2.reset_index().drop('index',axis = 1)

          layer1_neighbor_bts = []
          layer2_neighbor_bts = []
          if isinstance(df_neighbor_bts1.loc[0,'layer1_neighbor'],list) :
              layer1_neighbor_bts.extend(df_neighbor_bts1.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.extend(df_neighbor_bts1.loc[0,'layer2_neighbor'])
          else:
              layer1_neighbor_bts.append(df_neighbor_bts1.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.append(df_neighbor_bts1.loc[0,'layer2_neighbor'])
              
          if isinstance(df_neighbor_bts2.loc[0,'layer1_neighbor'],list):
              layer1_neighbor_bts.extend(df_neighbor_bts2.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.extend(df_neighbor_bts2.loc[0,'layer2_neighbor'])
          else:
              layer1_neighbor_bts.append(df_neighbor_bts2.loc[0,'layer1_neighbor'])
              layer2_neighbor_bts.append(df_neighbor_bts2.loc[0,'layer2_neighbor'])

# =============================================================================
# 开始规划邻区
# =============================================================================
     df_Scells = df_cell_info[df_cell_info['name'] == df_bts.loc[i,'name']]
     df_Scells = df_Scells[['Cell_name','Cell_index','azimuth','network','name']]
     df_Scells.rename(columns={'Cell_name':'Scell_name',
                              'Cell_index':'Scell_index',
                              'azimuth':'Scell_azimuth',
                              'network':'Scell_network',
                              'name':'S_name'
                              },inplace =True)
     df_Scells['assist'] = 'assist'

     df_layer1_cell = df_cell_info[df_cell_info['name'].isin(layer1_neighbor_bts)]
     df_layer1_cell = df_layer1_cell[['Cell_name','Cell_index','azimuth','network','name']]
     df_layer1_cell.rename(columns={'Cell_name':'Ncell_name',
                                   'Cell_index':'Ncell_index',
                                   'azimuth':'Ncell_azimuth',
                                   'network':'Ncell_network',
                                   'name':'N_name'
                                   },inplace =True)
     df_layer1_cell['assist'] = 'assist'


     df_layer2_cell = df_cell_info[df_cell_info['name'].isin(layer2_neighbor_bts)]
     df_layer2_cell = df_layer2_cell[['Cell_name','Cell_index','azimuth','network','name']]
     df_layer2_cell.rename(columns={'Cell_name':'Ncell_name',
                                   'Cell_index':'Ncell_index',
                                   'azimuth':'Ncell_azimuth',
                                   'network':'Ncell_network',
                                   'name':'N_name'
                                   },inplace =True)
     df_layer2_cell['assist'] = 'assist'

     df_layer1_neighbor = pd.merge(df_Scells,df_layer1_cell,how ='left', on = 'assist')
     df_layer1_neighbor['relation'] = df_layer1_neighbor['S_name'] + '_' + df_layer1_neighbor['N_name']
     df_layer1_neighbor['Degree'] = df_layer1_neighbor['relation'].map(Degree_dict)
     df_layer1_neighbor['add_neighbor'] = 'YES'

     df_layer2_neighbor = pd.merge(df_Scells,df_layer2_cell,how ='left', on = 'assist')
     df_layer2_neighbor['relation'] = df_layer2_neighbor['S_name'] + '_' + df_layer2_neighbor['N_name']
     df_layer2_neighbor['Degree'] = df_layer2_neighbor['relation'].map(Degree_dict)
     df_layer2_neighbor['add_neighbor'] = df_layer2_neighbor.apply(lambda x:plan_neighbor_cell(x.Degree,x.Scell_azimuth,x.Ncell_azimuth),axis=1)
     df_layer2_neighbor = df_layer2_neighbor[df_layer2_neighbor['add_neighbor'] == 'YES']

     df_plan_neighbor = df_layer1_neighbor.append(df_layer2_neighbor)
     plan_result.append(df_plan_neighbor)
     if i > 0 and i % 100 == 0:
          current_time = str(datetime.now()).split('.')[0]
          cur_time = time.time()
          print(current_time,' 总共：', str(len(df_bts)), '个小区 ，已完成：', str(i) ,'个小区。','花费时间',round(cur_time-start_time,0),'s !')
          print('预计还需要：',round((cur_time-start_time)*(len(df_bts)/(i+1) -1) ,0),'s!')
     elif i == len(df_bts)-1:
          current_time = str(datetime.now()).split('.')[0]
          print(current_time, '全部规划完成! 输出结果到文件。')
df_result = pd.concat(plan_result,axis = 0)
with open(data_path + '邻区规划结果.csv','w') as writer:
    df_result.to_csv(writer,index = False,chunksize = 10000)
print(current_time, '结果已输出到：',data_path,'邻区规划结果.csv')






