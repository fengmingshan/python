# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:16:03 2019

@author: Administrator
"""

# =============================================================================
# 枚举 - enumerate 可以有参数哦
# =============================================================================
list1 = ['a','b','c','d']
for i, item in enumerate(list1):
    print(i, item)


# enumerate迭代字符串
list(enumerate('abc'))
[(0, 'a'), (1, 'b'), (2, 'c')]

# enumerate也能指定起始index
list(enumerate('abc', 1))
[(1, 'a'), (2, 'b'), (3, 'c')]

# =============================================================================
# 字典列表推导式
# =============================================================================
my_dict = {i: i * i for i in range(100)}
my_set = {i * 15 for i in range(100)}

# =============================================================================
# 字符串直接转list
# =============================================================================
import ast
expr = "[1, 2, 3]"   # list字符串
expr2 = '[4,5,6]'   # list字符串
my_list = ast.literal_eval(expr)
my_list2 = ast.literal_eval(expr2)


# =============================================================================
# list 逆序
# =============================================================================
a = [1,2,3,4]
b = a[::-1] # -1表示逆序切片

a.reverse() # 原地逆序

# 字符串逆序
foo = "yasoob"
oof = foo[::-1]

# =============================================================================
# 三元运算
# =============================================================================

# [on_true] if [expression] else [on_false]
x, y = 50, 25

small = x if x < y else y
big = x if x > y else y

# =============================================================================
# 浅copy和 深copy
# =============================================================================
import copy
existing_list = [1,2,3,4]

new_list = existing_list
print(id(existing_list)) # 两个list的id一样在内存中同一个地址。
print(id(new_list))

new_list = copy.copy(existing_list)
print(id(existing_list)) # 两个list的id不同在内存中不同的地址。
print(id(new_list))

# =============================================================================
# 判断值是否相等,'=='对于值内存id相同才是True，对于其他数据类型，值相等就是True
# 'is'必须内存id相同才是True
# =============================================================================
import copy
a = 1234
b = copy.copy(a)
print(id(a)) # 两个list的id不同在内存中不同的地址。
print(id(b))
print(a == b)

list1 = [1,2,3,4]
list2 = copy.copy(list1)
print(id(list1)) # 两个list的id不同在内存中不同的地址。
print(id(list2))
print(list1 == list2)
print(list1 is list2)

list1 = [1,2,3,4]
list2 = list1
print(id(list1)) # 两个list的id相同
print(id(list2))
print(list1 == list2)
print(list1 is list2)

# =============================================================================
# list等可变对象做为函数的参数传入时，如果没有被显式的赋值，那么它将保留每一次对它的修改记录
# =============================================================================、
def generate_new_list_with(my_list=[], element=None):
    my_list.append(element)
    return my_list

list_1 = generate_new_list_with(element=1)
print(list_1)

list_2 = generate_new_list_with(element=2)
print(list_2)

list_3 = generate_new_list_with(element=3)
print(list_3)
# 为什么my_list没有被清空，因为 my_list是一个可变对象list。
# 当函数编译完成之后，再也没有对它进行过显式的赋值，
# 所以每运行一次函数它都会发生改变，并且一直携带着这些改变


# =============================================================================
# 解压函数 * 和 **, *可以解压list，**可以解压字典
# =============================================================================
def foo(x, y):
    print(x , y)

list1 = [1,2]
foo(*list1)

dict1 = {'x':1,'y':2}
foo(*dict1) # 解压key
foo(**dict1) # 解压value

a, b, *rest = range(10)
print(a)
print(b)
print(rest)

a,b,*rest,c = range(10)
print(a)
print(b)
print(rest)
print(c)


# =============================================================================
# 带名称的占位符,可读性更好
# =============================================================================
print("Hello %(name)s !" % {'name': 'James'})
print("I am years %(age)i years old" % {'age': 18})
print("Hello %(name)s ! I am years %(age)i years old" % {'name': 'James','age': 18})

print("Hello {name} !".format(name="James"))
print("I am years {age} years old".format(age="James"))
print("Hello {name}!I am years {age} years old".format(name="James",age = 18))

# =============================================================================
# 嵌套式列表推导式
# =============================================================================
[(i, j) for i in range(3) for j in range(i)]
[[i, j] for i in range(3) for j in range(i)]

string = 'abc'
[i+j+k for i in string for j in string.replace(i,'') for k in string.replace(i,'').replace(j,'')]

# =============================================================================
# 初始化元组
# =============================================================================
set1 = {1,2,3}
print(set1,type(set1))
set2 = set([1, 2, 3])
print(set2,type(set2))

# =============================================================================
# 切片删除list
# =============================================================================
list1 = [x for x in range(10)]
list1[3:6] = []

list2 = [x for x in range(10)]
del list2[3:6]

# =============================================================================
# isinstance可以判断多个属性，满足其中之一为True
# =============================================================================
print(1,'is float or int?',isinstance(1,(float, int)))
print(1.3,'is float or int?',isinstance(1.3, (float, int)))
print("\'1.3\'",'is float or int?',isinstance("1.3", (float, int)))
print("\'1.3\'",'is str or int?',isinstance("1.3", (str, int)))
