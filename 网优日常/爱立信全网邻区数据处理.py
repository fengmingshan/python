# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:32:01 2019

@author: Administrator
"""
import pandas as pd
import time

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
df_combined.drop('assist',axis = 0,inplace = True)

print('开始计算距离和夹角:')
start_time = time.time()
for i in range(len(df_eric800)):
     n = 0
     latA = df_eric800.loc[i,'LAT']
     lonA = df_eric800.loc[i,'LON']
     if i % 10 == 0 and  i/10 > 1 :
          current_time = time.time()
          print('已完成：',i,'个扇区。','花费时间',current_time-start_time,'s !')
          print('预计还需要：',round((current_time-start_time)*((len(df_eric800)/i)-1)/60,0),'分钟!')
     for j in range(len(df_all_cells)):
          if df_eric800.loc[i,'Cell_index'] != df_all_cells.loc[j,'Cell_index']:
               latB = df_all_cells.loc[j,'LAT']
               lonB = df_all_cells.loc[j,'LON']
               df_distance.loc[n,'Scell_index'] = df_eric800.loc[i,'Cell_index']
               df_distance.loc[n,'Scell_azimuth'] = df_eric800.loc[i,'azimuth']
               df_distance.loc[n,'Ncell_index'] = df_all_cells.loc[j,'Cell_index']
               df_distance.loc[n,'Ncell_azimuth'] = df_all_cells.loc[j,'azimuth']
               df_distance.loc[n,'Relations'] = str(df_eric800.loc[i,'Cell_index']) + '_' + str(df_all_cells.loc[j,'Cell_index'])
               n += 1

with pd.ExcelWriter(data_path + '邻区距离计算.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_distance.to_excel(writer,'邻区距离计算',index =False)

df_relations = df_distance[df_distance['Distance'] != 0]
for i in range(len(df_distance)):




