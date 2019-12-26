# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 10:59:16 2019

@author: Administrator
"""

import pandas as pd
import os

path = 'D:/_python小程序/3GI空闲CI核查'
os.chdir(path)
filename = os.listdir('./')[0]
os.startfile(path)

df = pd.read_csv('./' + filename ,engine = 'python' , encoding = 'utf-8')

ci_list = [x for x in range(54001,57999) if x not in set(df.全球小区号)]

df_res = pd.DataFrame({'空闲CI':ci_list})
with pd.ExcelWriter('./空闲CI.xlsx') as writer:
    df_res.to_excel(writer,index = False)