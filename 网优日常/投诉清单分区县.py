# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:02:49 2020

@author: Administrator
"""

import pandas as pd
import os
import numpy as np

work_path = 'D:/_python小程序/投诉清单添加区县'
os.chdir(work_path)
list_df = [pd.read_excel(file,header =0) for file in os.listdir('./')]
df_all = pd.concat(list_df,axis = 0)
df_all['区县'] = ''
def country(x):
    if '麒麟' in x:
        return '麒麟'
    elif '沾益' in x:
        return '沾益'
    elif '马龙' in x:
        return '马龙'
    elif '陆良' in x:
        return '陆良'
    elif '师宗' in x:
        return '师宗'
    elif '罗平' in x:
        return '罗平'
    elif '宣威' in x:
        return '宣威'
    elif '会泽' in x:
        return '会泽'
    elif '富源' in x:
        return '富源'
    else:
        return '未知'
df_all['区县'] = df_all['投诉内容'].map(lambda x:country(x))
df_all['区县'][df_all['区县'] == '未知'] = df_all['处理结果'][df_all['区县'] == '未知'].map(lambda x:country(x))
df_all['区县'].value_counts()
with pd.ExcelWriter('./汇总表_已分区县.xlsx') as f:
    df_all.to_excel(f,'汇总表',index =False)
