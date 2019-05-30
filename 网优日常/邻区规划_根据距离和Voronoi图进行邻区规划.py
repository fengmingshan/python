# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:37:13 2019

@author: Administrator
"""

import pandas as pd
import os
from math import ceil

max_neighbor_distance = 10000

distance_file= r'd:\_邻区自动规划\全网小区_距离计算结果.csv' +'\\'
cell_file =  r'd:\_爱立信全网邻区核查\全网小区.csv'
df_cell = pd.read_csv(cell_file , engine = 'python')

files  = os.listdir(path)
df_distance = pd.DataFrame()
for file in files:
     reader  = pd.read_csv(path + file , engine = 'python', iterator=True)
     loop = True
     chunkSize = 10000
     chunks = []
     while loop:
          try:
               chunk = reader.get_chunk(chunkSize)
               chunks.append(chunk)
          except StopIteration:
               loop = False
               print("Iteration is stopped.")
     df_tmp = pd.concat(chunks, ignore_index=True)
     df_distance = df_distance.append(df_tmp)
df_distance = df_distance.reset_index().drop('index',axis = 1)

df_cell_name = df_cell[['Cell_index','name','network']]
df_cell_name.rename(columns={'Cell_index':'Scell_index','name':'Scell_name','network':'Scell_network'},inplace =True)
df_distance = pd.merge(df_distance,df_cell_name,how = 'left', on = 'Scell_index')

df_cell_name.rename(columns={'Scell_index':'Ncell_index','Scell_name':'Ncell_name','Scell_network':'Ncell_network'},inplace =True)
df_distance = pd.merge(df_distance,df_cell_name,how = 'left', on = 'Ncell_index')

Scell_list = list(set(df_distance['Scell_index']))
for cell in Scell_list:
     df_tmp = df_distance[(df_distance['Scell_index'] == cell)&(df_distance['Distance'] <=max_neighbor_distance)]


