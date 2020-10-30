# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 16:54:01 2020

@author: Administrator
"""

# 获取连接
import pymssql
db = pymssql.connect('127.0.0.1', 'sa', 'ddh123', "aaa")

# 获取游标，相当于java中的Statement
cursor = db.cursor()

# 执行sql
sql = '''
    insert into t_user
      (username,password,age,height)
    values
      ('jlw', '23333', 31, 172)
'''
try:
   cursor = db.cursor()
   cursor.execute(sql)
   print('Successfu_sqlserver')
   db.commit()
except:
   print('Failed_sqlserver')
   db.rollback()

cursor.close()
db.close()