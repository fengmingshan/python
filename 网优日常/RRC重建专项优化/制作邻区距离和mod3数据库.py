# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:43:44 2020

@author: Administrator
"""

import pandas as pd
import os

work_path = r'C:\Users\Administrator\Desktop'
os.chdir(work_path)

L800_list = [17, 18, 19, 20, 21, 22,145, 146, 147, 148, 149,150]
L2100_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,129, 130, 131, 132, 133, 134, 135, 136]
L1800_list = [49, 50, 51, 52, 53, 54, 55, 56,177, 178, 179, 180, 181, 182]

def judge_mod3(scell_pci, scell_freq, ncell_pci, ncell_freq):
    if scell_freq == ncell_freq and scell_pci % 3 == ncell_pci % 3:
        return 1
    else:
        return 0

file_name = '邻区距离.csv'

df = pd.read_csv(file_name, encoding = 'utf-8')

df_pci = pd.read_csv('pci.csv', encoding = 'utf-8')

df.columns
df_pci.columns

df_pci = df_pci.set_index('cell_index')
dict_pci =df_pci['PCI'].to_dict()


df['scellpci'] = df['Scell'].map(dict_pci)
df['scellpci'].isnull().value_counts()

df['ncellpci'] = df['Ncell'].map(dict_pci)
df['ncellpci'].isnull().value_counts()

df['scell_id'] = df['Scell'].map(lambda x:int(x.split('_')[1]))
df['ncell_id'] = df['Ncell'].map(lambda x:int(x.split('_')[1]))

df['scell_freq'] = ''
df['ncell_freq'] = ''
df['scell_freq'][df['scell_id'].isin(L800_list)] = 'L800'
df['scell_freq'][df['scell_id'].isin(L2100_list)] = 'L2100'
df['scell_freq'][df['scell_id'].isin(L1800_list)] = 'L1800'

df['ncell_freq'][df['ncell_id'].isin(L800_list)] = 'L800'
df['ncell_freq'][df['ncell_id'].isin(L2100_list)] = 'L2100'
df['ncell_freq'][df['ncell_id'].isin(L1800_list)] = 'L1800'
df['ncell_freq'].unique()

df['ismod3'] = df.apply(lambda x:judge_mod3(x.scellpci, x.scell_freq, x.ncellpci, x.ncell_freq), axis =1)

df.columns

df = df[['relation', 'Scell', 'scellpci', 'scell_freq', 'Ncell', 'ncellpci',
       'ncell_freq', 'distance', 'ismod3']]

#df1 = df[df.scellpci.isnull()]
#df1.Scell.unique()
#
#df2 = df[df.ncellpci.isnull()]
#df2.Scell.unique()

with open('邻区距离_new.csv','w',newline = '') as f:
    df.to_csv(f,index =False)