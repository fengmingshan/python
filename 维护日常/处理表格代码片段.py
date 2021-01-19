# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 11:24:01 2021

@author: Administrator
"""

import pandas as pd
import os

path = r'D:\2021年工作\2021年无线维护团队KPI考核及薪酬分配\故障处理及时率计算'
file = '报表详单.xls'

os.chdir(path)

df = pd.read_excel(file, skip_rows = 0, header = 2)

