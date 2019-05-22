# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:32:01 2019

@author: Administrator
"""

import pandas as pd

data_path = r'd:\_爱立信全网邻区核查' + '\\'
file = r'd:\_爱立信全网邻区核查\PARA_ERBS_371.csv'

df_eric = pd.read_csv(file)

with pd.ExcelWriter(data_path + '爱立信全网邻区输出.xlsx') as writer: #不用保存和退出，系统自动会完成
    df_eric.to_excel(writer,'Sheet1',index =False)
