# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:31:57 2019

@author: Administrator
"""

import numpy as np
from tqdm import tqdm
import pandas as pd
import time

'''
在程序中添加炫酷的进度条
'''

df = pd.DataFrame(columns = ['area','province','city'],index = range(2000))
df['area'] = '中国云南曲靖'

def fill_province(x):
    x = x[2:4]
    # 这里加入时延是为了进度条显示效果
    time.sleep(0.001)
    return x

def fill_city(x):
    x = x[4:6]
    # 这里加入时延是为了进度条显示效果
    time.sleep(0.001)
    return x

df['province'] = pd.Series(fill_province(x) for x in tqdm(df['area']))
df['city'] = pd.Series(fill_city(x) for x in tqdm(df['area']))