# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 11:28:47 2018
在函数内部，可以调用其他函数。如果一个函数在内部调用自身本身，这个函数就是递归函数。
@author: Administrator
"""

"""
举个例子，我们来计算阶乘n! = 1 x 2 x 3 x ... x n，用函数fact(n)表示，可以看出：

fact(n) = n! = 1 x 2 x 3 x ... x (n-1) x n = (n-1)! x n = fact(n-1) x n

所以，fact(n)可以表示为n x fact(n-1)，只有n=1时需要特殊处理。
"""
#于是，fact(n)用递归的方式写出来就是：
def fact(n):         
    if n==1:
        return 1
    return n * fact(n - 1)
fact(1)
fact(5)

"""
使用递归函数需要注意防止栈溢出。在计算机中，函数调用是通过栈（stack）这种数据结构实现的，
每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。
由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出。可以试试fact(1000)：
解决递归调用栈溢出的方法是通过尾递归优化，事实上尾递归和循环的效果是一样的，
所以，把循环看成是一种特殊的尾递归函数也是可以的。
尾递归是指，在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。
这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，
不会出现栈溢出的情况。
上面的fact(n)函数由于return n * fact(n - 1)引入了乘法表达式，所以就不是尾递归了。
要改成尾递归方式，需要多一点代码，主要是要把每一步的乘积传入到递归函数中：
"""
#于是，fact(n)用尾递归的写法就是：
def fact_plus(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

#Python解释器没有对尾递归做优化，所以，即使把上面的fact(n)函数改成尾递归方式，也会导致栈溢出。

"""
实战练习：用递归函数非常简单地实现汉诺塔的移动
请编写move(n, a, b, c)函数，它接收参数n，表示3个柱子A、B、C中第1个柱子A的盘子数量，
然后打印出把所有汉诺塔圈从A借助B移动到C的方法，例如：
def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
如果是3层汉诺塔 move(3, 'A', 'B', 'C')
# 期待输出:
# A --> C
# A --> B
# C --> B
# A --> C
# B --> A
# B --> C
# A --> C
"""

# 利用递归函数移动汉诺塔:
def move(n, a, b, c):
    if n == 1:
        print('move', a, '-->', c)
    else:
        move(n-1, a, c, b)
        move(1, a, b, c)
        move(n-1, b, a, c)

move(4, 'A', 'B', 'C')


