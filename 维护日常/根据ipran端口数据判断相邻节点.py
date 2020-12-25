# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:13:06 2020

@author: Administrator
"""

import pandas as pd
import os

path = r'D:\_python小程序\通过ipran端口数据判断相邻节点'
file = 'ipran_全网端口描述.xls'
os.chdir(path)

df_port = pd.read_excel(file)
df_port.columns

equip_list = list(df_port['设备名称'].unique())