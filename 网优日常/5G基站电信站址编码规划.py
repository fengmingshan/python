# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:55:18 2020

@author: Administrator
"""

import pandas as pd
import os


def fill_zero(num):
    if len(str(num))<4:
        return str(0)*(4-len(str(num)))+str(num)
    else:
        return str(num)


path = r'D:\2020年工作\2020年8月5G规划站点'
os.chdir(path)

df = pd.read_excel('5G规划站点_电信站址编码对应表.xlsx')

区县 = ['沾益区', '宣威市', '师宗县', '经开区', '麒麟区', '马龙区', '罗平县', '陆良县', '会泽县',
       '富源县']
区县简称 = {
    '沾益区':'ZY',
    '宣威市':'XW',
    '师宗县':'SZ',
    '麒麟区':'QL',
    '马龙区':'ML',
    '罗平县':'LP',
    '陆良县':'LL',
    '经开区':'JK',
    '会泽县':'HZ',
    '富源县':'FY'
        }

for qx in 区县:
    qx_simple = 区县简称.get(qx)
    nums = [fill_zero(x) for x in range(1,len(df[df['区县'] == qx])+1)]
    bts_code = ['DXSWYNQJ5G{0}{1}'.format(qx_simple,num) for num in nums]
    df['电信站址编码'][df['区县'] == qx] = bts_code

with pd.ExcelFile('5G规划站点_电信站址编码对应表.xlsx') as f:
    df.to_excel(f,index = False)