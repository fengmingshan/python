# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:23:04 2019

@author: Administrator
"""

from numba import jit
import numpy as np

# 用numba加速的求和函数
@jit()
def nb_sum(a):
    Sum = 0
    for i in range(len(a)):
        Sum += a[i]
    return Sum

# 没用numba加速的求和函数
def py_sum(a):
    Sum = 0
    for i in range(len(a)):
        Sum += a[i]
    return Sum

a = np.linspace(0,100,100) # 创建一个长度为100的数组

%timeit np.sum(a) # numpy自带的求和函数
%timeit sum(a) # python自带的求和函数
%timeit nb_sum(a) # numba加速的求和函数
%timeit py_sum(a) # 没加速的求和函数

from math import sin

@nb.vectorize()
def nb_vec_sin(a):
    return sin(a)

%timeit np.sin(a) # numpy自带sin函数
%timeit nb_vec_sin(a) # numba加速的sin函数


import time
def foo(x,y):
        tt = time.time()
        s = 0
        for i in range(x,y):
                s += i
        print('Time used: {} sec'.format(time.time()-tt))
        return s

print(foo(1,100000000))




@jit
def numba_foo(x,y):
        tt = time.time()
        s = 0
        for i in range(x,y):
                s += i
        print('Time used: {} sec'.format(time.time()-tt))
        return s

print(numba_foo(1,100000000))





