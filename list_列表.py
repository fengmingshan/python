# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:29:44 2017

@author: Administrator
"""
#数据结构list
li1=[ 'abcd', 786 , 2.23, 'runoob', 70.2 ]
li2=[3,4,5]
print (li1) # 输出完整列表
print (li1[0]) # 输出列表第一个元素
print (li1[1:3]) # 从第二个开始输出到第三个元素
print (li1[2:]) # 输出从第三个元素开始的所有元素
print (li1* 2) # 输出两次列表
print (li1 + li2) # 连接列表
newlist=list+ li2
print(newlist)

#更新元素
list1 = ['Google', 'Runoob', 1997, 2000]
print ("第三个元素为 : ", list[2])
list1[2] = 2001
print ("更新后的第三个元素为 : ", list[2])

#添加元素
list1.append('obj')
list1

#删除元素
list2 = ['Google', 'Runoob', 1997, 2000]
print (list)
del list2[2]
print ("删除第三个元素 : ", list2)
list2.remove(2000)
print ("删除2000 : ", list2)

#计算元素个数
list3= ['Google', 'Runoob', 1997, 2000]
a= len(list)
print(a)

#list嵌套
a=['a','b','c']
n=[1,2,3]
dic= {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
x=[a,n,dic]
print(x)
print(x[0])
print(x[2])
print(x[0][1])

list4=[7,6,5,4,3,2,1]
list4.sort()
print(list1)

#list切片
list = ['x', 1, 'y', 2, 'z', 3]
list[::2]
list[1::2]


