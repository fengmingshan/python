# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:29:44 2017

@author: Administrator
"""
import copy

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

# 更新元素
list1 = ['Google', 'Runoob', 1997, 2000]
print ("第三个元素为 : ", list[2])
list1[2] = 2001
print ("更新后的第三个元素为 : ", list[2])

# 添加元素
list1.append('obj')
list1

# 删除元素
list2 = ['Google', 'Runoob', 1997, 2000]
print (list)
del list2[2]
print ("删除第三个元素 : ", list2)
list2.remove(2000)
print ("删除2000 : ", list2)
# =============================================================================
# 删除元素进阶，迭代删除
# =============================================================================
list1 = ['Google', 1997,'microsoft',1995,'tencent',1999]
# 我想通过迭代删除整个list, so easy是不是?

# 方法1：
for i in range(0,len(list1),1): # 年轻人,图样图森破!
    del list1[i]    # 报错了：list assignment index out of range ，index超出范围
print('new_list1=',list1)   #看看结果明明要删全部，结果[1997, 1995, 1999]逃过一劫

# 举个栗子：
list1 = ['Google', 1997,'microsoft',1995,'tencent',1999]
del list1[2] 
print('new_list1[2]=',list1[2]) 
# 删除了list1[2] 之后，后面的元素自动向上补位，导致新的list1[2] 变成了'1995'
# 如果采用迭代法，向上补位的元素就会躲过迭代，所以偶数位的[1997, 1995, 1999]逃过了删除

#方法2：
# 小样，我就不信治不了你！
list1 = ['Google', 1997,'microsoft',1995,'tencent',1999]
for element in list1: # 年轻人:图样图森破! * 2
    list1.remove(element)    
print('new_list1=',list1)  
# 没报错，但[1997, 1995, 1999]还在，通过元素迭代也是一样的，自动补位机制还是有效

# 方法3：
# 等等我知道你的套路了，我还有大招！
list1 = ['Google', 1997,'microsoft',1995,'tencent',1999]
def del_list(list_input,n):
    li_tmp1 = list_input[:n]
    li_tmp2 = list_input[n:]
    li_new = li_tmp1 + li_tmp2
    return li_new

for i in range(5,-1,-1):
    del_list(list1,i)
print('new_list1=',list1) # 等等，一个都没删掉？
# 年轻人:图样图森破! * 3！ list作为函数的参数传入时，在执行过程中不会改变原本的list。
        
# 正确的做法应该是：
list1 = ['Google', 1997,'microsoft',1995,'tencent',1999]
list2 =  copy.deepcopy(list1)   # 深拷贝，敲黑板使用 ‘=’赋值或者copy（）都是不行的
# 或者：list2 =  list1[:] 
for element in list2: 
    list1.remove(element)    
print('new_list1=',list1)   #这次list1终于变成空了，关于深拷贝和浅拷贝，见下面一节

# =============================================================================
# 进阶浅拷贝与深拷贝
# =============================================================================
list1 = ['Google', 'Runoob', 1997, 2000]
list2 = list1 
del list1[0]    # 删除list1的第一个元素：'Google'
print('list1=',list1)   # list1已经没有'Google'了
print('list2=',list2)   # 但是list2，也没有'Google'了
id(list1)   # 两个list的内存地址是一样的。针对一样的list电脑是不会浪费内存单独存储
id(list2)   # 只是把list1和list2的标签都指向同一个内存地址这就是：浅拷贝
list2 = copy.copy(list1) #这样也不行，还是浅拷贝
#要想深拷贝 要这样操作：
list2 = list1[:]
del list1[0] 
id(list1) # 这次地址不一样了
id(list2) 
# 或者这样
list2 = copy.deepcopy(list1) #深拷贝
id(list1)   # 地址也不一样了
id(list2)   #


# 计算元素个数
list3= ['Google', 'Runoob', 1997, 2000]
a= len(list)
print(a)

# list嵌套
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

# list切片
list = ['x', 1, 'y', 2, 'z', 3]
list[::2]
list[1::2]

# 生成器构造list
lis2=list(x+2 for x in lis1)

# map和 lambda
foo = [1, 2, 3, 4, 5]
map(lambda x: x + 10, foo)
map(lambda x: x*2, foo)
list(map(lambda x: x + 10, foo))
list(map(lambda x: x*2, foo))
print(list(map(lambda x: x + 10, foo)))
print(list(map(lambda x: x*2, foo)))



