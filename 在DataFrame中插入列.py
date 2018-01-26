# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 17:15:26 2018

@author: Administrator
"""

col_name = df.columns.tolist()  #获取df的列名，转换为list，赋值给col_name
col_name.insert(col_name.index('D'),'B')   # 在 col_name的‘B’ 列前面插入'D'
df.reindex(columns=col_name)  #重排df列的顺序 