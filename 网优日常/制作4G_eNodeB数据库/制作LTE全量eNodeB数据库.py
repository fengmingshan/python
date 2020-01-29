# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:35:39 2020

@author: Administrator
"""

import os
import pandas as pd

path = 'd:/Test'
os.chdir(path)
list_df = []
df1 = pd.DataFrame({'eNodeB' : range(729600,731648),'manufacturers' : '混合'})
list_df.append(df1)

df2 = pd.DataFrame({'eNodeB' : range(1019136,1019392),'manufacturers' : '爱立信'})
list_df.append(df2)

df3 = pd.DataFrame({'eNodeB' : range(582656,582912),'manufacturers' : '中兴'})
list_df.append(df3)

df4 = pd.DataFrame({'eNodeB' : range(585216,585472),'manufacturers' : '中兴'})
list_df.append(df4)

df5 = pd.DataFrame({'eNodeB' : range(588288,588416),'manufacturers' : '中兴'})
list_df.append(df5)

df6 = pd.DataFrame({'eNodeB' : range(588416,588544),'manufacturers' : '混合'})
list_df.append(df6)

df7 = pd.DataFrame({'eNodeB' : range(591104,591360),'manufacturers' : '中兴'})
list_df.append(df7)

df = pd.concat(list_df,axis = 0)
df.sort_values(by = 'eNodeB',ascending = True,inplace =True)
with open('./eNodeB.csv','a',encoding = 'utf-8') as f:
    df.to_csv(f,index = False)