# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:09:12 2019

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

df_cell_info = pd.read_csv(data_path + cell_info, engine = 'python' )
df_bts =  df_cell_info.drop_duplicates('name' ,keep = 'first')
df_bts = df_bts[['name','LON','LAT','azimuth']]
df_bts = df_bts.reset_index().drop('index',axis =1)

df_distance = pd.DataFrame(columns = ['S_bts_name','N_bts_name','Degree','Distance'])
#for i in range(len(df_bts)):
result = []
for i in range(2):
     df_tmp = pd.DataFrame(index = range(len(df_bts)))
     df_tmp['S_bts_name'] = df_bts.loc[i,'name']
     df_tmp['S_LON'] = df_bts.loc[i,'LON']
     df_tmp['S_LAT'] = df_bts.loc[i,'LAT']
     df_tmp['S_azimuth'] = df_bts.loc[i,'azimuth']
     df_tmp['N_bts_name'] = df_bts['name']
     df_tmp['N_LON'] = df_bts['LON']
     df_tmp['N_LAT'] = df_bts['LAT']
     df_tmp['S_azimuth'] = df_bts['azimuth']
     df_tmp['Degree'] = df_tmp.apply(lambda x :getDegree(x.S_LAT,x.S_LON,x.N_LAT,x.N_LON)\
           if (x.S_LAT != x.N_LAT) and (x.S_LON != x.N_LON) else 0,axis =1)
     df_tmp['Distance'] = df_tmp.apply(lambda x :getDistance(x.S_LAT,x.S_LON,x.N_LAT,x.N_LON)\
           if (x.S_LAT != x.N_LAT) and (x.S_LON != x.N_LON) else 0,axis =1)
     result.append(df_tmp)






