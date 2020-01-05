# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:41:10 2019

@author: Administrator
"""
import pandas as pd
import os

work_path = 'D:/Notebook/2019年12月_集团数里淘金竞赛_移动用户多分类'
os.chdir(work_path)

file_list = os.listdir('.')

# 读取数据
df_call = pd.read_csv('./data/call_data.csv',engine = 'python',encoding = 'utf-8')
df_customer = pd.read_csv('./data/cust_data.csv',engine = 'python',encoding = 'utf-8')
df_dpi = pd.read_csv('./data/dpi_data.csv',engine = 'python',encoding = 'utf-8')
df_period = pd.read_csv('./data/prd_data.csv',engine = 'python',encoding = 'utf-8')
df_terminal = pd.read_csv('./data/trmnl_data.csv',engine = 'python',encoding = 'utf-8')

df = pd.merge(df_call,df_customer,how = 'left' , on = 'user' )
df = pd.merge(df,df_dpi,how = 'left' , on = 'user' )
df = pd.merge(df,df_period,how = 'left' , on = 'user' )
df = pd.merge(df,df_terminal,how = 'left' , on = 'user' )

#with open('用户数据_合.csv','w') as writer:
#    df.to_csv(writer,index =False)

#df = pd.read_csv('用户数据_合.csv',engine = 'python')

# =============================================================================
# 数据清洗
# =============================================================================

# 查看有多少行存在缺失值
df_null = df[df.isnull().values==True].drop_duplicates()
len(df_null)
# 有16311行存在缺失值，所以必须要进行缺失值填充，不能简单的删除有缺失值的行

# 查看每个特征分别缺失了多少条记录
df_null.isnull().sum()

# 筛选出所有的有缺失值的特征名
df_feature = df.isnull().any()
df_null_feature = df_feature[df_feature==True]
null_feature = list(df_null.index)

# 统计该列空值的数量
# 统计某一列缺失值的数量
# 用户个人信息共有8个字段,其中有950条记录是全部特征都缺失，
# 这种记录即使通过填充补全得到的样本已经没有任何挖掘的价值，因为都是自己填充的假数据
df_customer.columns
df = df.dropna(subset=['cust_access_net_dt']) # 针对其中给一个特征删除空值就行了。

#with open('预处理_tmp.csv','w') as writer:
#    df.to_csv(writer,index =False)

df = pd.read_csv('预处理_tmp.csv',engine = 'python')
