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

df_data['退服时长(分钟)']=df_data['退服时长(分钟)'].astype(float)

df_eric=pd.read_excel(data_path+'\\'+eric_info,dtype =str,encoding='utf-8') 
df_eric=df_eric.set_index('SiteID')
dict_eric=df_eric.to_dict()
dict_eric=dict_eric['RRU中文名']
df_data.loc[0,'关联小区标识']=='nan'


for i in range(0,len(df_data),1):  
    if df_data.loc[i,'关联小区标识']=='nan':
        df_data.loc[i,'CELL_INDEX']=df_data.loc[i,'告警对象名称'].split('_')[0]+'_'+df_data.loc[i,'告警对象名称'].split('_')[0]  # 将基站名称切片得到基站等级
    else: 
        df_data.loc[i,'基站等级']=df_data.loc[i,'告警对象名称'].split('_')[2][1]   # 将基站名称切片得到基站等级
    if df_data.loc[i,'告警对象名称'] in dict_eric.keys():
        df_data.loc[i,'告警对象名称']=dict_eric[df_data.loc[i,'告警对象名称']]
    if '麒麟' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='麒麟'
    elif '沾益' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='沾益'
    elif '马龙' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='马龙'
    elif '陆良' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='陆良'
    elif '师宗' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='师宗'
    elif '罗平' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='罗平'
    elif '宣威' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='宣威'
    elif '会泽' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='会泽'
    elif '富源' in df_data.loc[i,'告警对象名称']:
        df_data.loc[i,'区县']='富源'
df_tmp=df_data[(df_data['基站等级']=='A')|(df_data['基站等级']=='B')]
df_sum_AB=df_tmp.groupby(by='区县',as_index=False).sum()
df_tmp=df_data[(df_data['基站等级']=='C')|(df_data['基站等级']=='D')]
df_sum_CD=df_tmp.groupby(by='区县',as_index=False).sum()
df_sum_CD=df_sum_CD.drop(0)
df_sum=pd.merge(df_sum_AB,df_sum_CD,how='left',on='区县')
df_sum=df_sum.rename(columns={'退服时长(分钟)_x':'A/B类平均断站时长','退服时长(分钟)_y':'C/D类平均断站时长'})

df_cell_num=pd.read_excel(data_path+'\\'+cell_num,dtype =str,encoding='utf-8')      #加入小区数量项 
df_sum=pd.merge(df_sum,df_cell_num,how='left',on='区县')
df_sum['小区数量']=df_sum['小区数量'].astype(int)
df_sum['A/B类小区数量']=df_sum['A/B类小区数量'].astype(int)
df_sum['C/D类小区数量']=df_sum['C/D类小区数量'].astype(int)

for i in range(0,len(df_sum),1):
    df_sum.loc[i,'A/B类平均断站时长']= df_sum.loc[i,'A/B类平均断站时长']/df_sum.loc[i,'A/B类小区数量']
    df_sum.loc[i,'C/D类平均断站时长']= df_sum.loc[i,'C/D类平均断站时长']/df_sum.loc[i,'C/D类小区数量']
df_sum=df_sum.sort_values(by='A/B类平均断站时长',ascending=True) # 根据退服时长升序排列
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
df_tmp=df_data[(df_data['基站等级']=='A')|(df_data['基站等级']=='B')]
df_sum.loc[9,'A/B类平均断站时长']=df_tmp['退服时长(分钟)'].sum()/df_sum['A/B类小区数量'].sum()
df_tmp=df_data[(df_data['基站等级']=='C')|(df_data['基站等级']=='D')]
df_sum.loc[9,'C/D类平均断站时长']=df_tmp['退服时长(分钟)'].sum()/df_sum['C/D类小区数量'].sum()
df_sum.loc[9,'小区数量']=df_sum['小区数量'].sum()
df_sum.loc[9,'A/B类小区数量']=df_sum['A/B类小区数量'].sum()
df_sum.loc[9,'C/D类小区数量']=df_sum['C/D类小区数量'].sum()
df_sum.loc[9,'A/B类断站排名']='---------'
df_sum.loc[9,'C/D类断站排名']='---------'

df_sum=df_sum.set_index(['区县'])

writer = pd.ExcelWriter(data_path+'\\'+'计算结果.xls') #输出到excel
df_sum.to_excel(writer, '断站时长汇总表')
writer.save()

