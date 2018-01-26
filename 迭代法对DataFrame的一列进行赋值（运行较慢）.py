# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:37:33 2018

@author: Administrator
"""

for i in range(0,df['第二列名'].count(),1):
        df.loc[i,0]= (df.iloc[i,1]== df.iloc[i,2])  
        #第一列的值等于（判断第二列和第三列是否相等返回的bool值）
        print(df.iloc[i,0])