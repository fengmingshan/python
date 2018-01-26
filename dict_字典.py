# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:18:06 2017
字典_数据结构:由键值对组成（键和对应的值，键是一个KEY,是不允许重复的，但是值可以重复），是无序的
@author: Administrator
"""
dict1 = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
dict2 = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
print ("dict2['Name']: ", dict2['Name'])
print ("dict2['Age']: ", dict2['Age'])

dict2['age']=8  #更新元素
dict2['school']='菜鸟教程'#增加元素
print ("dict2['age']: ", dict2['age'])
print ("dict2['school']: ", dict2['school'])
del dict2['age']
dict.clear()  #清除键值对，保留字典
del dict2   #删除整个字典

dict3 = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
dict3['school']= 'qujing'
len(dict3)