# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:53:21 2020

@author: Administrator
"""

import pandas as pd

df = pd.read_excel(r'C:\Users\Administrator\Desktop\hotmap.xlsx')
df.columns
with open(r'C:\Users\Administrator\Desktop\hotmap.txt', 'w') as f:
    f.writelines('    var points =['+'\n')
    for i in range(len(df)):
        f.writelines('{{"lng":{lon},"lat":{lat},"count":{num}}},'.format(lon=df.loc[i,'LONB'], lat=df.loc[i,'LATB'], num=df.loc[i,'PCI']))
        f.writelines('\n')
    f.writelines('];')
