# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:54:22 2021

@author: Administrator
"""

import pandas as pd
import os
import difflib

path = r'D:\_python小程序\通过ipran端口数据判断相邻节点'
on_loop_node = '在环上的关键传输节点_输出.xlsx'
os.chdir(path)

df_on_loop = pd.read_excel(on_loop_node)
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.split('-')[0])
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A1',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A2',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A3',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A4',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A5',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A6',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A7',''))
df_on_loop['归属A名称'] = df_on_loop['归属A名称'].map(lambda x:x.replace('A',''))

list_a_name = list(df_on_loop['归属A名称'])
df_on_loop.columns

最匹配基站名称 = []
for name in list_a_name:
    df_tmp = df_on_loop[df_on_loop['归属A名称'] == name]
    bts_matching_name = difflib.get_close_matches(name, df_tmp['现网基站名称'], cutoff = 0.3, n=1)[0] \
        if difflib.get_close_matches(name, df_tmp['现网基站名称'], cutoff = 0.3, n=1) \
        else ''
    df_tmp = df_tmp[df_tmp['现网基站名称'] == bts_matching_name]
    最匹配基站名称.append(df_tmp)
df_res = pd.concat(最匹配基站名称, axis = 0)
df_res =

with pd.ExcelWriter('成环的A设备关联铁塔站址.xlsx') as f:
    df_res.to_excel(f, index =False)