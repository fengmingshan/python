# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 19:29:39 2018

@author: Administrator
"""
import os
import pandas as pd
import math

pic_path = r'f:\资源照片一站一档'+'\\'
out_path = r'd:\test'+'\\'

pic_list = []
for root, dirs, files in os.walk(pic_path):
    for name in files:
        pic_list.append(os.path.join(root, name))
    
for i in range(0,math.ceil(len(pic_list)/10000),1):
    with open(out_path + '图片列表' + str(i) + '.csv' ,'w') as writer:
        df_out = pd.DataFrame()
        df_out['pic_path'] = ''
        if (i+1)*10000 < len(pic_list):
            for j in range(i*10000,(i+1)*10000,1):
                df_out.loc[j,'pic_path'] = pic_list[j]
            df_out.to_csv(writer)
        if (i+1)*10000 > len(pic_list):
            for j in range(i*10000,len(pic_list),1):
                df_out.loc[j,'pic_path'] = pic_list[j]
            df_out.to_csv(writer)



