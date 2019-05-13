# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:24:12 2019

@author: Administrator
"""

import pandas as pd 
import os
import numpy as np
from datetime import datetime 
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = r'D:\_VoLTE网络健康检查（日）\原始数据' + '\\'
out_path = r'D:\_VoLTE网络健康检查（日）' + '\\'
pic_path = r'D:\_VoLTE网络健康检查（日）\pic' + '\\'

s