# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:33:46 2020

@author: Administrator
"""

import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from math import sin
from math import cos
from math import tan
from math import asin
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
from math import sqrt
from math import ceil

path = r'D:\_python小程序\4G邻区距离计算'
os.chdir(path)

engine=create_engine('mysql+pymysql://root:a123456@218.63.75.43:3306/hand_over?charset=utf8',echo=False)
DBSession=sessionmaker(bind=engine)
session=DBSession()

rela = session.execute("SELECT CONCAT(`eNodeB`,'_',`小区`) as Scell , 邻区关系 as Ncell  FROM `邻区切换`")
rela = list(rela)
Scells =  [str(x.Scell) for x in rela]
Ncells =  [str(x.Ncell) for x in rela]
df_relation = pd.DataFrame({
    'Scell':Scells,
    'Ncell':Ncells,
    })
df_relation['relation'] = df_relation['Scell']+'_'+df_relation['Ncell']

df_lonlat = pd.read_csv('./4G基站经纬度.csv', engine = 'python')
df_lonlat.set_index('CELL',inplace = True)
dict_lon = df_lonlat['LON'].to_dict()
dict_lat = df_lonlat['LAT'].to_dict()

def calc_Distance(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)]) # 经纬度转换成弧度
    dlon = lon2-lon1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance,0)
    return distance


df_relation['SLON'] = df_relation['Scell'].map(dict_lon)
df_relation['SLAT'] = df_relation['Scell'].map(dict_lat)
df_relation['NLON'] = df_relation['Ncell'].map(dict_lon)
df_relation['NLAT'] = df_relation['Ncell'].map(dict_lat)
df_relation['distance'] = df_relation.apply(lambda x:calc_Distance(x.SLON,x.SLAT,x.NLON,x.NLAT),axis =1)
df_relation = df_relation[~df_relation['distance'].isnull()]
Base = declarative_base()   #创建对象Base将ORM基类declarative_base()实例化
class Relation_distance(Base):  #这里的User是ORM对象，user是数据库中的表格，通过定义类将表user与类User建立了关联
    # 表的名字:
    __tablename__ = '邻区距离'
    # 表的结构:
    relation = Column(String(200), primary_key=True)
    Scell = Column(String(200))
    Ncell = Column(String(200))
    distance = Column(Float(20))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine) #调用父类Base类中的方法（函数）.create_all创建表结构
#session.rollback()
session.commit()    #确认修改
session.close()     #关闭会话

relation_distance = [Relation_distance(
    relation=relation,
    Scell=scell,
    Ncell=ncell,
    distance=distance
    )
    for relation,scell,ncell, distance in
        zip(
            df_relation['relation'],
            df_relation['Scell'],
            df_relation['Ncell'],
            df_relation['distance']
        )]

for item in relation_distance:
    session.add(item)

session.commit()
session.close()     #关闭会话

