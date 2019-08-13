# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:24:13 2019

@author: Administrator
"""

import pandas as pd
import os

data_path = r'd:\test' + '\\'

carrier_files = [x for x in os.listdir(data_path) if '载频无线参数表' in  x ]
hardware_files = [x for x in os.listdir(data_path) if '物理资产' in  x ]

df_carrier = pd.DataFrame()
for file in carrier_files:
     df_tmp = pd.read_excel(data_path + file,skiprows = 1)
     df_carrier = df_carrier.append(df_tmp)
