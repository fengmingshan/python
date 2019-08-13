# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:16:44 2019

@author: Administrator
"""
import pandas as pd
import os

data_path = r'd:\2019年工作\2019年8月4G网络扩频方案\NE_4HLR_20190811' + '\\'
file_names = [x for x in os.listdir(data_path) if '.txt' in x]
number_imsi_dict = dict()
for name in file_names:
     file_details  = open(data_path + name)
     lines = file_details.readlines()
     for line in lines:
          content = list(filter(None,line.split(' ')))
          number = int(content[0][2:-3])
          imsi = '46003' + content[2]
          number_imsi_dict[number] = imsi

df_number_imsi = pd.DataFrame()
df_number_imsi['号码'] = number_imsi_dict.keys()
df_number_imsi['IMSI'] = number_imsi_dict.values()

with open(data_path + 'number_imsi.csv','w') as writer:
    df_number_imsi.to_csv(writer,index =False)

