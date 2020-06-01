# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:17:41 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

# =============================================================================
# 通过生成器读取大型 excel 文件
# =============================================================================
def read_csv_partly(file):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=100000)
    for df_tmp in file_data:
        yield df_tmp

# =============================================================================
# 将包含多个值的一列拆分成多列
# =============================================================================
import pandas as pd

df = pd.DataFrame({'Country':['China','US','Japan','EU','UK/Australia', 'UK/Netherland'],
               'Number':[100, 150, 120, 90, 30, 2],
               'Value': [1, 2, 3, 4, 5, 6],
               'label': list('abcdef')})
df

df_new = df.drop('Country', axis=1).join(df['Country'].str.split('/',
                expand=True).stack().reset_index(level=1, drop=True).rename('Country'))
# 过程分步介绍
df['Country'].str.split('/', expand=True).stack()
df['Country'].str.split('/', expand=True).stack().reset_index(level=1, drop=True)
df['Country'].str.split('/', expand=True).stack().reset_index(level=1, drop=True).rename('Country')
