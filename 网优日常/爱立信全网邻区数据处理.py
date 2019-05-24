# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:32:01 2019

@author: Administrator
"""
import os 
import pandas as pd
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


data_path = r'd:\_爱立信全网邻区核查' + '\\'
eric_neighbor = r'd:\_爱立信全网邻区核查\PARA_ERBS_371.csv'
zte_neighbor = r'd:\_爱立信全网邻区核查\ZTE_neighbors.xlsx'
zte_eric800 = r'd:\_爱立信全网邻区核查\爱立信云南曲靖电信工参表20190428.xlsx'
zte_bts800 = r'd:\_爱立信全网邻区核查\曲靖电信LTE工参(L800M)20190425.xls'
zte_bts1800 = r'd:\_爱立信全网邻区核查\曲靖电信LTE工参(L1.8G)20190425.xls'

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

start_time = time.time()

df_eric = pd.read_csv(eric_neighbor,engine = 'python')

df_eric_result = pd.DataFrame()
df_eric_result['Scell_index'] = df_eric['CELL'].map(lambda x:x.split('_')[0] + x.split('_')[1])
df_eric_result['Ncell_index'] = df_eric['EUTRANCELLRELATIONID'].map(lambda x:x.replace('46011-','').replace('-',''))
df_eric_result['Relations'] = df_eric_result['Scell_index'] + '_' + df_eric_result['Ncell_index']

df_zte_result = pd.read_excel(zte_neighbor)
df_zte_result['relation'] = df_zte_result['Scell_index'].map(str) + '_' + df_zte_result['Ncell_index'].map(str)

df_all_neighbors = df_eric_result.append(df_zte_result)

df_tmp = pd.read_excel(zte_bts800)
df_zte800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_zte800['eNodeB_ID'] = df_tmp['ENODEBID']
df_zte800['Cell_name'] = df_tmp['CELLNAME']
df_zte800['Cell_index'] = df_tmp['ENODEBID'].map(str)  + df_tmp['CELLID'].map(str)
df_zte800['LON'] = df_tmp['LONC']
df_zte800['LAT'] = df_tmp['LATC']
df_zte800['azimuth'] = df_tmp['Azimuth']
df_zte800['network'] = 'L800'
df_zte800['manufacturers'] = 'ZTE'

df_tmp = pd.read_excel(zte_bts1800)
df_zte1800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_zte1800['eNodeB_ID'] = df_tmp['ENODEBID']
df_zte1800['Cell_name'] = df_tmp['CELLNAME']
df_zte1800['Cell_index'] = df_tmp['ENODEBID'].map(str)  + df_tmp['CELLID'].map(str)
df_zte1800['LON'] = df_tmp['LONC']
df_zte1800['LAT'] = df_tmp['LATC']
df_zte1800['azimuth'] = df_tmp['Azimuth']
df_zte1800['network'] = 'L1.8'
df_zte1800['manufacturers'] = 'ZTE'

df_tmp = pd.read_excel(zte_eric800)
df_eric800 =pd.DataFrame(columns = ['eNodeB_ID','Cell_name','Cell_index','LON','LAT','azimuth','network','manufacturers'])
df_eric800['eNodeB_ID'] = df_tmp['eNBId']
df_eric800['Cell_name'] = df_tmp['Cell_name']
df_eric800['Cell_index'] =  df_tmp['Cell_index']
df_eric800['LON'] = df_tmp['longitude']
df_eric800['LAT'] = df_tmp['latitude']
df_eric800['azimuth'] = df_tmp['azimuth']
df_eric800['network'] = df_tmp['channelBandwidth'].map({'5M':'L800M', '15M':'L1.8'})
df_eric800['manufacturers'] = 'ERIC'

df_all_cells = df_zte800.append(df_zte1800).append(df_eric800)
df_all_cells = df_all_cells.reset_index()

cur_time = time.time()
current_time = str(datetime.now()).split('.')[0]
print(current_time,':','基站基础信息处理完成，开始生成邻区关系对。','\n','累计额花费时间:',round(cur_time-start_time,0),'s！')

df_Scells = pd.DataFrame()
df_Scells['Scell_index'] = df_eric800['Cell_index']
df_Scells['Scell_azimuth'] = df_eric800['azimuth']
df_Scells['Scell_LON'] = df_eric800['LON']
df_Scells['Scell_LAT'] = df_eric800['LAT']

df_Ncells = pd.DataFrame()
df_Ncells['Ncell_index'] = df_all_cells['Cell_index']
df_Ncells['Ncell_azimuth'] = df_all_cells['azimuth']
df_Ncells['Ncell_LON'] = df_all_cells['LON']
df_Ncells['Ncell_LAT'] = df_all_cells['LAT']

df_Scells['assist'] = 'assist'
df_Ncells['assist'] = 'assist'
df_combined = pd.merge(df_Scells,df_Ncells,how = 'left',on ='assist' )
df_combined.drop('assist',axis = 1,inplace = True)

cur_time = time.time()
current_time = str(datetime.now()).split('.')[0]
print(current_time,':','邻区关系对生成完成，开始计算邻区距离和夹角。','\n','累计额花费时间:',round(cur_time-start_time,0),'s！')

for i in range(ceil(len(df_combined)/1000000)):
    df_combined.loc[i*1000000:(i+1)*1000000,].to_csv(data_path + '邻区关系对_'+ str(i) + '.csv',index =False)

all_files= os.listdir(data_path)
relation_files = [x for x  in all_files if '邻区关系对' in x ]

calc_time = time.time()
for file in relation_files:
    df_calculated = pd.DataFrame()
    df_relation = pd.read_csv(data_path + file)
    calc_cell = list(set(df_relation['Scell_index']))
    for i in range(len(calc_cell)):
         df_tmp = df_combined[df_combined['Scell_index'] == calc_cell[i]]
         df_tmp1 = df_tmp[(df_tmp['Scell_LAT'] != df_tmp['Ncell_LAT'])&
                          (df_tmp['Scell_LON'] != df_tmp['Ncell_LON'])]
         df_tmp1['Degree'] = df_tmp1.apply(lambda x :getDegree(x.Scell_LAT,x.Scell_LON,x.Ncell_LAT,x.Ncell_LON),axis =1)
         df_tmp1['Distance'] = df_tmp1.apply(lambda x :getDistance(x.Scell_LAT,x.Scell_LON,x.Ncell_LAT,x.Ncell_LON),axis =1)
         df_tmp2 = df_tmp[(df_tmp['Scell_LAT'] == df_tmp['Ncell_LAT'])&
                          (df_tmp['Scell_LON'] == df_tmp['Ncell_LON'])]
         df_tmp2['Degree'] = 0
         df_tmp2['Distance'] = 0
         df_calculated = df_calculated.append(df_tmp1).append(df_tmp1)
    df_calculated.to_csv(data_path  + '邻区距离计算结果_' + file.split('.')[0][-1:] + '.csv' , index =False)
    cur_time = time.time()
    current_time = str(datetime.now()).split('.')[0]
    print(current_time,' 已完成：',file.split('.')[0][-1:],'个扇区。','花费时间',round(cur_time-calc_time,0),'s !')
    print('预计还需要：',round((cur_time-calc_time)*(37/int(file.split('.')[0][-1:])-1),0),'s!')

cur_time = time.time()
current_time = str(datetime.now()).split('.')[0]
print(current_time,':','计算完成，开始筛选适合的邻区。','\n','累计额花费时间:',round(cur_time-start_time,0),'s！')




