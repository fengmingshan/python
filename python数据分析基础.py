# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:08:16 2017
数据分析numpy,pandas库
@author: Administrator
"""
import pandas as pd
import numpy as np

X=pd.Series(['a',True,1])  
x= pd.Series([1,2,4],index=['a','b','d'])
n=pd.Series(['3'],index=['c'])
x=x.append(n)
print (x['a'],x['b'],x['c'],x['d'])

print (x[0],x[1],x[2],x[3])
x= x.reindex(['a','b','c','d'])  #重排序
print (x['a'],x['b'],x['c'],x['d'])

print(1 in x.values)

df= pd.DataFrame(data ={'age':[21,22,23],'name':['Ken','John','JiMi']},index=['a','b','c'])
print(df.iloc[0:1,0:1])
print(df.iloc[0:2,0:1])
print(df.iloc[0:3,0:1])
print(df.iloc[0:1,0:1])
print(df.iloc[0:2,0:2])
print(df[1:2])

df.colums=['age1','name1']
df.index=['0','1','2']
dfnew=df.drop('a',axis=0)
dfnew=df.drop('age',axis=1)

r=np.arange(1,20,1)
r2= r[r>5]       

df2= pd.DataFrame(data ={'col1':[1,2,3],'col2':[4,5,6],'col3':[7,8,9]},index=['0','1','2'])
result = df2+df2
result = df2*df2
result = np.power(df2,2)

df3 = pd.DataFrame(data ={'col1':np.random.randn(5),'col2':np.random.randn(5),'col3':np.random.randn(5)},index=['0','1','2','3','4'])
df3['Row_sum']=df3.apply(lambda x:x.sum(),axis=1)  #增加一列对行求和，axis=1表示跨列取数，因为是对行求和所以要一行行取数。
df3.loc['Col_sum']=df3.apply(lambda x:x.sum(),axis=0)  #在末尾增加一行对列求和，axis=0表示跨行取数，因为是对列求和所以要一列列取数。

#数据导入-cvs
import pandas as pd
df4 = pd.read_csv(r'd:\python\telecom_train.csv',encoding='utf-8')    #导入一张CSV表格
df41 = pd.read_excel(r'd:\python\telecom_train.xls',encoding='utf-8')    #导入一张excel97,2003表格

#数据库连接,导出
import pandas as pd
from sqlalchemy import create_engine
engine=create_engine('mysql+pymysql://root:123456@218.63.75.42:3306/铁塔租费?charset=utf8',echo=False)
df5=pd.read_sql('select * from employees.departments',engine)      #导入数据库中的表格 
df51=pd.read_sql('select * from v_full_departement_fms',engine)    #导入数据库中做好的视图
