# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 09:29:43 2018
MYSQL数据库连接操作
连接数据库要使用到pandas和sqlalchemy两个库。命令格式：
MySQL-Python
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]

MySQL-Connector
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
@author: Administrator
"""
import pandas as pd   
from sqlalchemy import create_engine   #这里格式不一样，是因为我们只用用到create_engine这个函数，所以可以只导入一个模块，不用导入整个sqlalchemy库
from sqlalchemy.orm import sessionmaker



engine=create_engine('mysql+pymysql://root:123456@218.63.75.42:3306/话务周报?charset=utf8',echo=False)
'''
这里的engine是一个对象，用来打开数据库，数据库的IP地址：218.63.75.42:3306 数据库名：话务周报 用户名：root 密码：123456。
echo = True 是为了方便 控制台 logging 输出一些sql信息，默认是False
通过这个engine对象可以直接execute 进行查询，例如 engine.execute("SELECT * FROM user") 
也可以通过 engine 获取连接在查询，例如 conn = engine.connect() DBsession=sessionmaker(bind=engine) 
通过 conn.execute("SELECT * FROM user")或者session.execute('select * from 3g话务量')方法进行查询。
两者有什么差别呢？
直接使用engine的execute执行sql的方式, 叫做connnectionless执行,有些复杂的查询很难写，因为格式容易出错
借助 engine.connect()获取conn, 然后通过conn执行sql, 叫做connection执行--官方推荐
'''


#无连接方式：打开数据库中的表格，注意，这里小括号里面用的是MYSQL的语句，所以你在MYSQL学的语句统统都可以用了。可以实现很强大的取数操作
df1=pd.read_sql('select * from 3g话务量',engine)      #导入数据库话务周报中的表格： 3g话务量

df2=pd.read_sql('select * from 小区登记对象',engine)      #导入数据库话务周报中的表格： 小区登记对象

df3=pd.read_sql('select * from 3g话务量周报',engine)      #导入数据库话务周报中的视图： 3g话务量周报，视图打开会很慢。因为还有复杂的查询运算

df4=pd.read_sql('select SUM(`1X: 小区CS呼叫话务量(Erl)`) from 3g话务量 GROUP BY `cell`',engine)   #导入数据库话务周报中的表格： 3g话务量,带筛选条件


#用连接方式打开数据库中的表格
conn=engine.connect()   #连接数据库

result1=conn.execute('select * from 3g话务量')     #选取表3g话务量，使用connection方式访问数据库得到的不是表格而是一个result。需要通过迭代才能取出内容
result2=conn.execute('select * from 小区登记对象 where 定时登记成功次数>300') #选取表小区登记对象
#主语这里出来的不是
for row1 in result1:
    print('BTS:', row1['BTS'])
for row2 in result2:
    print('次数:', row2['定时登记成功次数'])
conn.close()

#用session方式打开数据库中的表格
#本质上session还是使用MYSQL命令来操作

engine1=create_engine('mysql+pymysql://root:123456@218.63.75.42:3306/test?charset=utf8',echo=False)
DBSession=sessionmaker(bind=engine1) 
session=DBSession()
result1=session.execute('select * from 3g话务量')  #使用session方式访问数据库得到的不是表格而是一个result。需要通过迭代才能取出内容
result2=session.execute('select * from 小区登记对象 where 定时登记成功次数=200')
for row1 in result1:
    print('BTS:', row1['BTS'])
for row2 in result2:
    print('次数:', row2['定时登记成功次数'])
conn.close()


