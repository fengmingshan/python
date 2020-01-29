# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:22:42 2019

@author: Administrator
"""

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


