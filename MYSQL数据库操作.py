# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 09:29:43 2018
MYSQL数据库连接操作
连接数据库要使用到pandas和sqlalchemy两个库
@author: Administrator
"""
import pandas as pd   
from sqlalchemy import create_engine   #这里格式不一样，是因为我们只用用到create_engine这个函数，所以可以只导入一个模块，不用导入整个sqlalchemy库
from pandas import DataFrame as DF     #这里我从pandas库导入了数据框-DataFrame这种数据格式,并命名为df。以后就可以直接使用DataFrame了

a=DF(columns=['区县','支局','站址名称','话务量'])  #因为我之前已经导入了数据框-DataFrame这种数据格式，所以直接可以直接新建一个数据框。

b=pd.DataFrame(columns=['区县','支局','站址名称','话务量'])    #如果不导入DataFrame这种数据格式，代码就要这样写，比较复杂，不方便阅读

#好了，下面开始连接数据库了
engine=create_engine('mysql+pymysql://root:123456@218.63.75.42:3306/话务周报?charset=utf8',echo=False)
#这里的engine是一个变量，用来打开数据库，数据库的IP地址：218.63.75.42:3306 数据库名：话务周报 用户名：root 密码：123456

#打开数据库中的表格，注意，这里小括号里面用的是MYSQL的语句，所以你在MYSQL学的语句统统都可以用了。可以实现很强大的取数操作
df1=pd.read_sql('select * from 3g话务量',engine)      #导入数据库话务周报中的表格： 3g话务量

df2=pd.read_sql('select * from 小区登记对象',engine)      #导入数据库话务周报中的表格： 小区登记对象

df3=pd.read_sql('select * from 3g话务量周报',engine)      #导入数据库话务周报中的视图： 3g话务量周报，视图打开会很慢。因为还有复杂的查询运算

df4=pd.read_sql('select SUM(`1X: 小区CS呼叫话务量(Erl)`) from 3g话务量 GROUP BY `cell`',engine)   #导入数据库话务周报中的表格： 3g话务量,带筛选条件




