# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:04:21 2019

@author: Administrator
"""

import pandas as pd
import os

data_path = r'd:\test' + '\\'

carrier_files = [x for x in os.listdir(data_path) if '载频无线参数表' in  x ]
hardware_files = [x for x in os.listdir(data_path) if '物理资产' in  x ]

def completion_town_name(df,col_name):
     df[col_name] = df[col_name].map(lambda x:x.replace('十八','十八连山'))
     df[col_name] = df[col_name].map(lambda x:x.replace('黄泥','黄泥河'))
     df[col_name] = df[col_name].map(lambda x:x.replace('大莫','大莫古'))
     df[col_name] = df[col_name].map(lambda x:x.replace('小百','小百户'))
     df[col_name] = df[col_name].map(lambda x:x.replace('三岔','三岔河'))
     df[col_name] = df[col_name].map(lambda x:x.replace('八大','八大河'))
     df[col_name] = df[col_name].map(lambda x:x.replace('大水','大水井'))
     df[col_name] = df[col_name].map(lambda x:x.replace('旧屋','旧屋基'))
     df[col_name] = df[col_name].map(lambda x:x.replace('鲁布','鲁布革'))
     df[col_name] = df[col_name].map(lambda x:x.replace('王家','王家庄'))
     df[col_name] = df[col_name].map(lambda x:x.replace('马过','马过河'))
     df[col_name] = df[col_name].map(lambda x:x.replace('白石','白石江'))
     return df

df_carrier = pd.DataFrame()
for file in carrier_files:
     df_tmp = pd.read_excel(data_path + file,skiprows = 1)
     df_carrier = df_carrier.append(df_tmp)
df_carrier.columns
df_carrier['区县'] = df_carrier['bts_alias'].map(lambda x:x.split('QJ')[1][0:2])
df_carrier['乡镇'] = df_carrier['bts_alias'].map(lambda x:x.split('QJ')[1][2:4])
df_carrier['乡镇_feature'] = df_carrier['bts_alias'].map(lambda x:x.split('QJ')[1][4:5])
df_carrier = completion_town_name(df_carrier,'乡镇')

list_city = ['中安','金钟','中枢','罗雄','通泉','白石江','建宁','寥廓','南宁','丹凤','宛水','西宁','双龙','虹桥','西平',]
df_carrier_city = df_carrier[(df_carrier['乡镇'].isin(list_city))\
                             &(~df_carrier['bts_alias'].str.contains('村'))\
                             &(~df_carrier['bts_alias'].str.contains('屯'))\
                             &(~df_carrier['bts_alias'].str.contains('营'))\
                             &(~df_carrier['bts_alias'].str.contains('寨'))\
                             &(~df_carrier['bts_alias'].str.contains('坪'))\
                             &(~df_carrier['bts_alias'].str.contains('井'))\
                             &(~df_carrier['bts_alias'].str.contains('潭'))\
                             &(~df_carrier['bts_alias'].str.contains('水库'))\
                             &(~df_carrier['bts_alias'].str.contains('接入网'))\
                             &(~df_carrier['bts_alias'].str.contains('山'))]

df_carrier_town = df_carrier[df_carrier['乡镇_feature'].str.contains('乡')\
                             |df_carrier['乡镇_feature'].str.contains('镇')\
                             |df_carrier['乡镇_feature'].str.contains('电')]

df_city_town = df_carrier_city.append(df_carrier_town)

with  open(data_path  + '乡镇以上载频数据.csv','w')  as writer:  #输出到excel
   df_city_town.to_csv(writer, index = False)
