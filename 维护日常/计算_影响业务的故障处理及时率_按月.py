# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:04:41 2020

@author: Administrator
"""

import os
import pandas as pd

path = r'D:\2020年工作\2020年9月维护团队KPI考核办法\故障详单'
os.chdir(path)
file = '影响业务的故障.xlsx'

city = [
    'FYSJ',
    'FYZA',
    'HZJZ',
    'LLBQ',
    'LPLX',
    'QLSB',
    'QLXC',
    'QLXX',
    'SZCY',
    'XWBQ',
    'XWXN',
    '富源胜境',
    '富源中安',
    '会泽金钟',
    '陆良同乐',
    '陆良中枢',
    '罗平罗雄',
    '马龙通泉',
    '麒麟白石',
    '麒麟建宁',
    '麒麟寥廓',
    '麒麟南宁',
    '麒麟三宝',
    '麒麟太和',
    '麒麟文华',
    '麒麟西城',
    '麒麟潇湘',
    '麒麟沿江',
    '麒麟珠街',
    '师宗丹凤',
    '宣威板桥',
    '宣威虹桥',
    '宣威双龙',
    '宣威宛水',
    '宣威西宁',
    '沾益XP',
    '沾益西平']

df = pd.read_excel(file)
#df.columns
df['简称'] = ''
df['城区农村'] = ''
df['简称'] = df['网元/IP/局站'].map(lambda x: x.split('QJ')[1][:4])
df['城区农村'] = df['简称'].map(lambda x:'城区' if x in city else '农村')
df['有效处理时长(分)'] = df['有效处理时长(分)'].astype(float)
city_dict = dict()
villag_dict = dict()
for month in df['月份'].unique():
    df_city = df[(df['月份'] == month)&(df['城区农村'] == '城区')]
    df_village = df[(df['月份'] == month)&(df['城区农村'] == '农村')]
    city_in_time = len(df_city[df_city['有效处理时长(分)']<4320])/len(df_city)
    village_in_time = len(df_village[df_village['有效处理时长(分)']<5760])/len(df_village)
    city_dict.update({month:city_in_time})
    villag_dict.update({month:village_in_time})
