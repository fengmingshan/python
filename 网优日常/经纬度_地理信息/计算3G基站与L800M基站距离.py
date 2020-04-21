# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 11:21:13 2020

@author: Administrator
"""

import pandas as pd
import os
import sys
from tqdm import tqdm

sys.path.append('d:/_python/python/custom-package/')
from lon_lat_calc import calc_Distance

work_path = 'd:/_python小程序/根据经纬度计算基站间距离/'
os.chdir(work_path)
files = os.listdir()

df_source = pd.read_excel('3G.xlsx', encoding='utf-8')
df_destnation = pd.read_excel('800M.xlsx', encoding='utf-8')
df_source.loc[0,:]
df_destnation.loc[0,:]

df_res = pd.DataFrame(
    columns=[
        '源基站ID',
        '源基站名',
        '源基站经度',
        '源基站纬度',
        '目标基站ID',
        '目标基站名',
        '目标基站经度',
        '目标基站纬度',
        '距离'])
df_res['源基站ID'] = tqdm([x for x in df_source['基站代码'] for y in df_destnation['基站代码']])
df_res['源基站名'] = tqdm([x for x in df_source['基站名称']
                       for y in df_destnation['基站名称']])
df_res['源基站经度'] = tqdm([x for x in df_source['LON'] for y in df_destnation['LON']])
df_res['源基站纬度'] = tqdm([x for x in df_source['LAT'] for y in df_destnation['LAT']])
df_res['目标基站ID'] = tqdm([y for x in df_source['基站代码'] for y in df_destnation['基站代码']])
df_res['目标基站名'] = tqdm([y for x in df_source['基站名称']
                        for y in df_destnation['基站名称']])
df_res['目标基站经度'] = tqdm([y for x in df_source['LON'] for y in df_destnation['LON']])
df_res['目标基站纬度'] = tqdm([y for x in df_source['LAT'] for y in df_destnation['LAT']])
df_res['距离（米）'] = tqdm([calc_Distance(a, b, c, d) for a, b, c, d in zip(
    df_res['源基站经度'], df_res['源基站纬度'], df_res['目标基站经度'], df_res['目标基站纬度'])])

df_min_distance = df_res.groupby(['源基站ID', '源基站名', '源基站经度', '源基站纬度'], as_index=False)['距离（米）'].agg(min)
df_no_neighbor = df_min_distance[df_min_distance['距离（米）'] >= 1000]

with pd.ExcelWriter('距离计算结果.xlsx') as writer:
    df_min_distance.to_excel(writer , '与800G基站最小距离', index=False)
    df_no_neighbor.to_excel(writer , '3G孤站', index=False)
