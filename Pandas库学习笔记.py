# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 16:56:01 2018

@author: Administrator
  pandas库 和  numpy库 学习笔记
"""
import pandas as pd   #导入pandas库
from pandas import DataFrame   #从pandas库导入数据框这种数据结构
import numpy as np   #导入numpy库

"""
DataFram的创建
"""
randn=np.random.randn(8,5) #使用numpy的randn函数构造一个8行5列的数组
randn                 #显示数组randn

alist=np.arange(1,9,1) #使用numpy的range函数构造一个list以1开头8结束，每一跳为1的数组，用于做行号
alist

blist = list('ABCDE') #构建一个5位的list用于做列标，
blist

df=pd.DataFrame(randn,index=alist,columns=blist)  #构建一个以alist为行标，blist为列标的数据框
df

pd.DataFrame(data=None,index=None,columns=None,dtype=None,copy=False)
#DataFrame的参数，data是要转换成DataFrame的内容（如字典，元组等）如果是元祖转换的话"键"就是列名.
#index是索引，columns是列名，dtype是数据类型copy暂时不用关注。

df2=pd.DataFrame(randn)   #  转换成DataFrame时，未指定index和cloumns，系统自动设定，从0开始。
df2

"""
修改行、列名
"""

#修改列名,方法一：暴力方法

df.columns = ['a','b','c','d','e']

#修改列名,方法二：字典法，可读性较好的方法

df.rename(columns={'A':'a', 'B':'b', 'C':'c','D':'d','E':'e'}, inplace = True)  
#inplace= True表示修改完以后直接覆盖掉原DataFrame不用再赋值

#好处是可以随意改个数：
df.rename(columns={'A':'a', 'C':'c'}, inplace = True)

"""
在表格中插入列
"""

col_name = df.columns.tolist()  #获取df的列名，转换为list，赋值给col_name
col_name.insert(col_name.index('D'),'B')   # 在 col_name的‘D’ 列前面插入'B'
df.reindex(columns=col_name)  #重排df列的顺序 


"""
数据筛选
"""

df[df['A']>0]  #筛选A列大于0的数据
df[(df['A']>0)&(df['B']>0)]  #筛选A，B列都大于0的数据
df[(df['A']>0)|(df['B']>0)]  #筛选A，B列其中一列大于0的数据
df[['A','B']][df['A']>0]     #只显示A,B两列，筛选A列大于0的数据

df1 = pd.read_excel(r'd:\python\sell_df1.xls',encoding='utf-8')    #导入一张excel97,2003表格
df1

df1[df1['区县'].isin(['麒麟','沾益'])]  #精确筛选出df1中，区县一列等于麒麟和马龙。
df1[df1['区县'].str.contains('马')]     #模糊筛选出df1中，区县一列等于包含'马'的。
df1[df1['区县'].str.contains('马|沾')]     #模糊筛选出df1中，区县一列等于包含'马'和'沾'的。
#注意模糊筛选条件里面不支持'&'。.str不能省略，因为Series数组没有Contains函数，必须先转成str才行

""" 
Apply函数实例:
Apply 函数是处理数据和建立新变量的常用函数之一。
在向数据框的每一行或每一列传递指定函数后，Apply 函数会返回相应的值。
这个由 Apply 传入的函数可以是系统默认的或者用户自定义的。
例如，在下面的例子中它可以用于统计每一行和每一列中的缺失值。或则对行或者列求和
"""

def num_missing(x):   #定义统计缺失值的数量的函数num_missing:
  return sum(x.isnull())

def get_sum(x):       #定义统计求和的函数get_sum:
    try:
        return sum(x)
    except:
        return '总计'
    
#Applying 对每列运用查缺函数:
print ('Missing values per column:')
print(df.apply(num_missing,axis=0)) #axis=0 按列执行
 
#Applying 对每行运用查缺函数:
print ('nMissing values per row:')
print(df.apply(num_missing, axis=1).head()) #axis=1 按行执行

df.loc['求和']=df.apply(get_sum)  #在数据框最后面面添加一行对数据框进行求和

df['行求和']=df.apply(get_sum,axis=1)  #在数据框最后面添加一行对数据框的行进行求和
df



""" 
merge 函数实例:
how=left/inner/right/outer,
inner只合并两表的公共行，left只合并左表中有的行，right只合并右表中有的行，outer合并两个表中所有的行
"""
df1 = pd.read_csv(r'd:\python\telecom_train.csv',encoding='utf-8') #导入一张csv表格

df1 = pd.read_excel(r'd:\python\sell_df1.xls',encoding='utf-8')    #导入一张excel97,2003表格
df2 = pd.read_excel(r'd:\python\sell_df2.xls',encoding='utf-8')    #导入一张excel97,2003表格

df3=pd.merge(df1,df2,how='inner',left_on='门店',right_on='门店')     #根据门店关键字对两张表进行合并
df3

df4=pd.merge(df1,df2,how='inner',on='门店')  #因为 两列中都有相同的关键字'门店'所以可以简写为on='门店'
df4

df5=pd.merge(df1,df2,how='inner',on='门店',suffixes=('_左表','_右表'))  #两个表中相同的列名加上不同的标签
df5

df6=pd.merge(df1[['区县','门店','销售']],df2[['门店','上月销售']],how='inner',on='门店')  #只选取需要的列，inner合并
df6

df7=pd.merge(df1[['区县','门店','销售']],df2[['门店','上月销售']],how='outer',on='门店')  #只选取需要的列，outer合并
df7


"""
写入到excel，多次写入多页
"""
#如果直接使用to_excel是不行的，每一次写入操作都会将原来的excel表格覆盖掉，最终只能的得到最后一次的写入结果
df1.to_excel(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls', sheet_name='本月变化订单')
df2.to_excel(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls', sheet_name='本月新增订单')

#在同一张表格中多次写入不同的页
with pd.ExcelWriter(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls') as writer:
    df1.to_excel(writer, '本月变化订单')
    df2.to_excel(writer, '本月新增订单')

# 数据透视表
df_sum=pd.pivot_table(df_data,values='退服时长(分钟)',index=['区县','基站等级'],aggfunc='sum')
