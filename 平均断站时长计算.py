# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:25:13 2018
结果输出在e:\_断站目录下，计算结果.xls表格中
@author: Administrator
"""

import os
import sys
import pandas as pd
#确定该程序是python脚本还是封装的exe文件
eric_info=r'Eric_info.xls'
cell_num=r'cell_num.xls'

data_path = r'd:\data'

df_data=pd.DataFrame()
files=os.listdir(data_path)    #返回指定目录下的所有文件和目录名

for filename in files:
    if filename!=r'cell_num.xls' and filename!=r'Eric_info.xls' and  filename!=r'计算结果.xls':
        file=data_path+'\\'+filename
        df_tmp=pd.read_excel(file,skiprows=1,dtype =str,encoding='utf-8') 
        df_data=df_data.append(df_tmp,ignore_index=True)        
col_name = df_data.columns.tolist()  #获取df的列名，转换为list，赋值给col_name
col_name.insert(col_name.index('统计时间'),'区县')   # 在 col_name的‘统计时间’ 列前面插入'区县'
df_data=df_data.reindex(columns=col_name)  #重排df列的顺序     
df_data.loc[:,'区县']=''
df_data['告警对象名称']=df_data['告警对象名称'].map(lambda x: x.replace('GCTC',''))
df_data['告警对象名称']=df_data['告警对象名称'].map(lambda x: x.replace('调测-',''))
df_data['告警对象名称']=df_data['告警对象名称'].map(lambda x: x.replace('调测_',''))
df_data['告警对象名称']=df_data['告警对象名称'].map(lambda x: x.replace('整治_',''))

for i in  range(0,len(df_data),1): 
    if df_data.loc[i,'关联小区标识']=='nan':
        df_data.loc[i,'关联小区标识']=df_data.loc[i,'告警对象名称'].split('_')[0]+'_'+df_data.loc[i,'告警对象名称'].split('_')[1]
    df_data.loc[i,'关联小区数量']=len(df_data.loc[i,'关联小区标识'].split(','))
df_data['退服时长(分钟)']=df_data['退服时长(分钟)'].astype(float)
df_data['关联小区数量']=df_data['关联小区数量'].astype(int)
df_data['小区退服时长']=df_data['退服时长(分钟)']/df_data['关联小区数量']
df_data['小区退服时长']=df_data['小区退服时长'].map(lambda x: round(x,2))

df_cell_list=pd.read_excel(data_path+'\\'+cell_num,sheetname='cell_list',dtype =str,encoding='utf-8')      #加入小区数量项 

cell_break=()   # 新建一个元组用来统计所有发生退服的小区
for i in range(0,len(df_data),1):
    cell_break=cell_break + tuple(df_data.loc[i,'关联小区标识'].split(','))

for i in range(0,len(df_cell_list),1):
    if df_cell_list.loc[i,'CELL_INDEX'] in cell_break:
        df_cell_list.loc[i,'退服']=1
df_cell_break=df_cell_list[df_cell_list['退服']==1]
df_cell_break=df_cell_break.reset_index()
df_cell_break=df_cell_break.drop('index',axis=1)

for i in range(0,len(df_cell_break),1):   
    break_time =[]      # 创建一个空list，用来装一个小区的退服时长
    for j in range(0,len(df_data),1):
        if df_cell_break.loc[i,'CELL_INDEX'] in df_data.loc[j,'关联小区标识'].split(','):
             break_time.append(df_data.loc[j,'小区退服时长'])
    df_cell_break.loc[i,'小区退服时长']=sum(break_time)   # 一个小区的退服时长求和 

df_tmp=df_cell_break[['区县','小区退服时长']][(df_cell_break['小区等级']=='A')|(df_cell_break['小区等级']=='B')]
df_sum_AB=df_tmp.groupby(by='区县',as_index=False).sum()
df_tmp=df_cell_break[['区县','小区退服时长']][(df_cell_break['小区等级']=='C')|(df_cell_break['小区等级']=='D')]
df_sum_CD=df_tmp.groupby(by='区县',as_index=False).sum()
df_sum=pd.merge(df_sum_AB,df_sum_CD,how='left',on='区县')
df_sum=df_sum.rename(columns={'小区退服时长_x':'A/B类平均断站时长','小区退服时长_y':'C/D类平均断站时长'})

df_cell_num=pd.read_excel(data_path+'\\'+cell_num,sheetname='cell_num',dtype =str,encoding='utf-8')      #加入小区数量项 
df_sum=pd.merge(df_sum,df_cell_num,how='left',on='区县')
df_sum['小区数量']=df_sum['小区数量'].astype(int)
df_sum['A/B类小区数量']=df_sum['A/B类小区数量'].astype(int)
df_sum['C/D类小区数量']=df_sum['C/D类小区数量'].astype(int)

for i in range(0,len(df_sum),1):
    df_sum.loc[i,'A/B类平均断站时长']= df_sum.loc[i,'A/B类平均断站时长']/df_sum.loc[i,'A/B类小区数量']
    df_sum.loc[i,'C/D类平均断站时长']= df_sum.loc[i,'C/D类平均断站时长']/df_sum.loc[i,'C/D类小区数量']

df_sum=df_sum.sort_values(by='A/B类平均断站时长',ascending=True) # 根据A/B类平均断站时长升序排列
df_sum=df_sum.reset_index()
del df_sum['index']
for i in range(0,len(df_sum),1):
    df_sum.loc[i,'A/B类断站排名']=i+1

df_sum=df_sum.sort_values(by='C/D类平均断站时长',ascending=True) # 根据退服时长升序排列
df_sum=df_sum.reset_index()
del df_sum['index']
for i in range(0,len(df_sum),1):
    df_sum.loc[i,'C/D类断站排名']=i+1

df_sum['A/B类平均断站时长']=df_sum['A/B类平均断站时长'].map(lambda x: round(x,2))
df_sum['C/D类平均断站时长']=df_sum['C/D类平均断站时长'].map(lambda x: round(x,2))
df_sum['A/B类断站排名']=df_sum['A/B类断站排名'].astype(int)
df_sum['C/D类断站排名']=df_sum['C/D类断站排名'].astype(int)

df_sum.loc[9,'区县']='全市'
df_tmp=df_cell_break[['区县','小区退服时长']][(df_cell_break['小区等级']=='A')|(df_cell_break['小区等级']=='B')]
df_sum.loc[9,'A/B类平均断站时长']=df_tmp['小区退服时长'].sum()/df_sum['A/B类小区数量'].sum()
df_tmp=df_cell_break[['区县','小区退服时长']][(df_cell_break['小区等级']=='C')|(df_cell_break['小区等级']=='D')]
df_sum.loc[9,'C/D类平均断站时长']=df_tmp['小区退服时长'].sum()/df_sum['C/D类小区数量'].sum()
df_sum.loc[9,'小区数量']=df_sum['小区数量'].sum()
df_sum.loc[9,'A/B类小区数量']=df_sum['A/B类小区数量'].sum()
df_sum.loc[9,'C/D类小区数量']=df_sum['C/D类小区数量'].sum()
df_sum.loc[9,'A/B类断站排名']='---------'
df_sum.loc[9,'C/D类断站排名']='---------'

df_sum=df_sum.set_index(['区县'])

writer = pd.ExcelWriter(data_path+'\\'+'计算结果.xls') #输出到excel
df_sum.to_excel(writer, '断站时长汇总表')
writer.save()

