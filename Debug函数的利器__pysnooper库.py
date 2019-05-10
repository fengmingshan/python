# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 19:35:41 2018

@author: Administrator
"""

import pysnooper
import random

@pysnooper.snoop()
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

number_to_bits(6)


def foo():
    lst = []
    for i in range(10):
        lst.append(random.randrange(1, 1000))

    with pysnooper.snoop():
        lower = min(lst)
        upper = max(lst)
        mid = (lower + upper) / 2
        print(lower, mid, upper)
foo()

# 针对函数内出现循环，pysnooper也能展开到每一层循环：
@pysnooper.snoop()
def sum2(x):
    for i in range(0,50,1):
        x = x+i 
        print(x)
    
sum2(2)


def sum2(x,y):
    for i in range(0,50,1):
        z = x + y + i 
        print(z)
        with pysnooper.snoop():
            sum_xy = x + y
            count = i
            print(sum_xy, count)

sum2(1,2)



    