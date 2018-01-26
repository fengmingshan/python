# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 15:46:02 2018

@author: Administrator
"""

import pandas as pd
df4 = pd.read_csv(r'd:\python\telecom_train.csv',encoding='utf-8')    #导入一张CSV表格
df5 = pd.read_excel(r'd:\python\telecom_train.xls',encoding='utf-8')    #导入一张excel97,2003表格

df4 .to_csv(r'd:\python\telecom_train.csv',encoding='utf-8')    #导入一张CSV表格
df4 .to_excel(r'd:\python\telecom_train.csv',encoding='utf-8')    #导入一张CSV表格


"""
写入到excel，多次写入多页
"""
#如果直接使用to_excel是不行的，每一次写入操作都会将原来的excel表格覆盖掉，最终只能的得到最后一次的写入结果
df1.to_excel(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls', sheet_name='本月变化订单')
df2.to_excel(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls', sheet_name='本月新增订单')

#在同一张表格中多次写入不同的页
writer = pd.ExcelWriter(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls')
df1.to_excel(writer, '本月变化订单')
df2.to_excel(writer, '本月新增订单')
writer.save()

