# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 22:43:25 2018

@author: Administrator
"""
#一个简单的函数
def foo():
    print('i am foo')

#现在有一个新的需求，希望可以记录下函数的执行日志，于是在代码中添加日志代码
import logging

def foo():
    print('i am foo')
    logging.info('foo is running')

#其他函数bar()、bar2()也有类似的需求，怎么做？在每个函数代码里面都添加logging语句吗？

#简单的装饰器
def use_logging(func):
    def warpper(*args,**kwargs):
        logging.warning('%s is running' % func.__name__ )
        return func(*args,**kwargs)
    return warpper

def bar():
    print('i am bar')

bar = use_logging(bar)
bar()

#这样写还是不方便，我们每次都要将一个函数作为参数传递给use_logging函数。
#所以引入了语法糖@符号是装饰器的语法糖
@use_logging    # 表示下面这个函数被use_logging装饰器装饰过了
def foo():
    print("i am foo")    
foo()

@use_logging    # 表示下面这个函数被use_logging装饰器装饰过了
def bar():
    print("i am bar")
bar()    

#带参数的装饰器
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warning("%s is running" % func.__name__)
            return func(*args)
        return wrapper
    return decorator

#当我们使用@use_logging(level="warn")调用的时候，Python能够发现这一层的封装，并把参数传递到装饰器的环境中。
@use_logging(level="warn")
def foo(name='foo'):
    print("i am %s" % name)
    
foo()

#类装饰器:使用类来定义装饰器
#类装饰器还可以依靠类内部的__call__方法，当使用 @ 形式将装饰器附加到函数上时，就会调用__call__里面此方法。


class Foo(object):
    def __init__(self,func):
        self._func = func

    def __call__(self):
        print ('class decorator runing')
        self._func()
        print ('class decorator ending')
@Foo
def bar():
    print ('bar')

bar()


# 使用装饰器极大地复用了代码,但是他有一个缺点就是原函数的元信息不见了，比如函数的docstring、__name__、参数列表，
#先看例子：有一个数学运算的函数
def f(x):
    """does some math"""
    return x + x * x
print(f.__name__)   # 它有自己的名称
print(f.__doc__)    # 也有自己的说明文字__doc__

#定义装饰器
def logged(func):
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
   return x + x * x
#函数f被with_logging取代了，当然它的docstring，__name__就是变成了with__logging函数的信息了。
print(f.__name__)
print(f.__doc__)

# 这个问题在某些轻卡是较严重的
# 好在我们有functools.wraps，wraps本身也是一个装饰器，它能把原函数的元信息拷贝到装饰器函数中，
# 这使得装饰器函数也有和原函数一样的元信息了。
from functools import wraps

def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
   return x + x * x

print(f.__name__)   # 现在打印函数的名称和doc，和原函数一样了
print(f.__doc__)

#python内置装饰器
#@staticmathod、@classmethod、@property

#装饰器的顺序
@a
@b
@c
def f ():
    print('xxx')
#等效于
f = a(b(c(f)))


