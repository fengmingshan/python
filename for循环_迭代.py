# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 11:26:48 2018
如果给定一个list或tuple，我们可以通过for循环来遍历这个list或tuple，
这种遍历我们称为迭代（Iteration）。
Python的for循环不仅可以用在list或tuple上，还可以作用在其他可迭代对象上。
list这种数据类型虽然有下标，但很多其他数据类型是没有下标的，
但是，只要是可迭代对象，无论有无下标，都可以迭代，
@author: Administrator
"""
# list可以迭代：
print('for x in iter([1, 2, 3, 4, 5]):')
for x in iter([1, 2, 3, 4, 5]):
    print(x)

# iter迭代器也可以迭代：
print('next():')
it = iter([1, 2, 3, 4, 5])
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))

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
for v in d.values():
    print('value:', v)

# iter both key and value:
print('iter item:', e)
for k, v in d.items():
    print('item:', k, v)

# 默认情况下，dict迭代的是key。因为dict是无序的，所以，两次迭代出的结果顺序很可能不一样。
# 如果要迭代value，可以用for value in d.values()。
# 如果要同时迭代key和value，可以用for k, v in d.items()。

# 划重点，由于字符串也是可迭代对象，因此，也可以作用于for循环：
for ch in 'ABCDE':
    print(ch)

#划重点，如何判断一个对象是可迭代对象呢？方法是通过collections库的Iterable类型判断：
from collections import Iterable  # 导入collections库
isinstance('abc', Iterable)     # str是否可迭代
isinstance([1,2,3], Iterable)   # list是否可迭代
isinstance(123, Iterable)   # 整数是否可迭代

from collections import Iterable, Iterator
def g():
    yield 1
    yield 2
    yield 3
print('Iterable? [1, 2, 3]:', isinstance([1, 2, 3], Iterable))
print('Iterable? \'abc\':', isinstance('abc', Iterable))
print('Iterable? 123:', isinstance(123, Iterable))
print('Iterable? g():', isinstance(g(), Iterable))
print('Iterator? [1, 2, 3]:', isinstance([1, 2, 3], Iterator))
print('Iterator? iter([1, 2, 3]):', isinstance(iter([1, 2, 3]), Iterator))
print('Iterator? \'abc\':', isinstance('abc', Iterator))
print('Iterator? 123:', isinstance(123, Iterator))
print('Iterator? g():', isinstance(g(), Iterator))


# 如果要对list实现类似Java那样的下标循环怎么办？
# Python内置的enumerate函数可以把一个list变成索引-元素对，
# 这样就可以在for循环中同时迭代索引和元素本身：
for i, value in enumerate(['A', 'B', 'C']):   # 这里用enumerate函数把list变成了索引和值两列
    print(i, value)

#上面的for循环里，同时引用了两个变量，在Python里是很常见的，比如下面的代码：
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)
  
# 练习题，请使用迭代查找一个list中最小和最大值，并返回一个tuple： 
# list1=[2,5,7,8,3,9]   

def findMinAndMax(L):
    if len(L)<1:
        L_min=None
        L_max=None
    else: 
        L_min=L[0]
        L_max=L[0]
        for i in L:
            if i>L_max:
                L_max=i
            elif i<L_min:
                L_min=i            
    return (L_min,L_max)
   
# 可以使用下面的代码，对所写的代码进行测试。
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')
