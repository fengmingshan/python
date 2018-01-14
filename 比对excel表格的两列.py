# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:35:04 2018

@author: Administrator
"""
import pandas as pd   #导入pandas库
from pandas import DataFrame   #从pandas库导入数据框这种数据结构
import numpy as np   #导入numpy库


#导入上月账单和本月账单
df_old = pd.read_excel(r'd:\2018年工作\2018年铁塔租费核对\tower_201709.xls',dtype =str,encoding='utf-8')    #导入上月铁塔账单
df_new = pd.read_excel(r'd:\2018年工作\2018年铁塔租费核对\tower_201710.xls',dtype =str,encoding='utf-8')    #导入本月铁塔账单    

#手动比较方法
df_change_tmp=df_merge.iloc[:,[6+146,7+146,10,10+146]]    #取左表的第10列和右表的第十列构建一个新DataFrame：df_change_tmp
df_change_tmp.columns = ['铁塔站址名称','铁塔站址编码''上月值','本月值'] #修改新表的列标
df_change_tmp.insert(0,'变化内容',df_merge.columns[10][:-2])  #在df_change_tmp最前面插入一列 '变化内容'，该列的内容=左表第十列的列标去掉最右边3个字符'_左表'
df_change_tmp.insert(0,'发生变化',0)  #在df_change_tmp最前面插入一列 '发生变化',内容=0
df_change_tmp['发生变化']=~(df_change_tmp.iloc[:,4]==df_change_tmp.iloc[:,5])   #对df_change_tmp列进行赋值=比较df_change_tmp第4列和第5列是否相等，然后取反
df_change=df_change_tmp[df_change_tmp['发生变化']==True]   #对df_change_tmp筛选，'属性变化'列=True的内容，赋值给我们需要的结果df_change

#循环比较方法
for i in range(11,147,1):
    df_change_tmp=df_merge.iloc[:,[7+146,8+146,i,i+146]]
    df_change_tmp.columns = ['铁塔站址名称','铁塔站址编码''上月值','本月值']
    df_change_tmp.insert(0,'变化内容',df_merge.columns[i][:-2])
    df_change_tmp.insert(0,'发生变化',0)
    df_change_tmp['发生变化']=~(df_change_tmp.iloc[:,2]==df_change_tmp.iloc[:,3])
    df_change_tmp=df_change_tmp[df_change_tmp['发生变化']==True]
    df_change=pd.concat([df_change,df_change_tmp[df_change_tmp['发生变化']==True]])
