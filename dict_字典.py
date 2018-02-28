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
dict3['Name']
s='Name'
dict3[s]

#字典的初始化
d={}  
s = [('Tom', 5), ('Jone', 2), ('Susan', 4), ('Tom', 4), ('Tom', 1)]  

for i,j in s:  
    d[i]=j  
print(d)
for i in d.keys():
    print(i)  

#字典的迭代
# dict没有序号但也可以迭代：
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)

# dict根据三种值进行迭代：
e = {'a': 1, 'b': 2, 'c': 3}
# iter each key:
print('iter key:', e)
for k in d.keys():
    print('key:', k)

# iter each value:
print('iter value:', e)
for k in d.values():
    print('value:', v)

# iter both key and value:
print('iter item:', e)
for k, v in d.items():
    print('item:', k, v)

# 默认情况下，dict迭代的是key。因为dict是无序的，所以，两次迭代出的结果顺序很可能不一样。
# 如果要迭代value，可以用for value in d.values()。
# 如果要同时迭代key和value，可以用for k, v in d.items()。


#字典的初始化
k={}  
s = [('Tom', 5), ('Jone', 2), ('Susan', 4), ('Tom', 4), ('Tom', 1)]  
for i,j in s:  
    if i not in k.keys():#注意不能写成 if not k[i],因为其返回值不是None,而是error  
        l=[]  
        l.append(j)  
        k[i]=l  
    else:  
        k[i].append(j)  
print(k)  


#字典的初始化
from collections import defaultdict  
d=defaultdict(list)  
s = [('Tom', 5), ('Jone', 2), ('Susan', 4), ('Tom', 4), ('Tom', 1)]  
for i,j in s:  
    d[i].append(j)  
print(list(d.items()))  

from collections import defaultdict  
d=defaultdict(set)  
s = [('Tom', 5), ('Jone', 2), ('Susan', 4), ('Tom', 4), ('Tom', 1)]  
for i,j in s:  
    d[i].add(j)  
print(list(d.items()))  

#字典的操作获取所有key
info = dict(name='cold', blog='linuxzen.com')
info.keys()

#获取key,value并循环
info = dict(name='cold', blog='linuxzen.com')
for key, value in info.items():
    print key, ':',  value
