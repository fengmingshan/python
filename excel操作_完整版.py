# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 19:35:41 2018

@author: Administrator
"""
#==============================================================================
# 打开excel表格
#==============================================================================
df=pd.read_excel(file,dtype =str,encoding='utf-8') 
df=pd.read_excel(file,skiprows=1,dtype =str,encoding='utf-8')  # skiprows=1跳过1行
df=pd.read_excel(file,sheetname='sheet1',dtype =str,encoding='utf-8') # sheetname='sheet1'指定读取得sheet名

df=pd.read_csv(file,dtype =str,encoding='utf-8') 


#==============================================================================
# 写入到excel表格，to_excel没有追加写入模式，会覆盖表格原来的内容，to_csv有追加写入模式
#==============================================================================
writer = pd.ExcelWriter('output.xlsx')
df1.to_excel(writer,'Sheet1') 
df2.to_excel(writer,'Sheet2',index=False) # index=False不带row index输出
writer.save()

writer = pd.ExcelWriter('output.xlsx')
df1.to_excel(writer,'Sheet1',columns=False,index=False) # 不带行名和列名输出
df2.to_excel(writer,'Sheet1',startrow=5,sol=5) # 可以将两个df写入到一个sheet，指定写入的起始位置
writer.save()

df_sum.to_csv(r'd:\data\计算结果.csv')
df_cell_num.to_csv(r'd:\data\计算结果.csv',mode='a') # to_csv有追加写入模式不会覆盖原来的内容

help(pd.read_csv)
