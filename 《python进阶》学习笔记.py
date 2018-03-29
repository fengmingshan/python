# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 22:55:20 2018

@author: Administrator
"""
# =============================================================================
# *args 和 **kwargs
# =============================================================================
#其实并不是必须写成*args 和**kwargs。 只有变量前面的 *(星号)才是必须的. 
#你也可以写成*var 和**vars. 而写成*args 和**kwargs只是一个通俗的命名约定。 
def test_args_kwargs(*args,**kwargs ):
    print("arg:", args)
    print("kwargs:", kwargs)

def another_test_args_kwargs(*var,**vars):
    print("var:", var)
    print("vars:", vars)
# 这两种写法是一样的
 test_args_kwargs(test, name = 'xxx')
 another_test_args_kwargs(test, name = 'xxx')
 # 两种写法运行效果完全一样，所以以后你不用纠结*args 和 **kwargs了


# =============================================================================
# *args 的用法
# =============================================================================
# *args是用来发送一个非键值对的可变数量的参数列表给一个函数.
def test_var_args(f_arg, *argv):
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)

test_var_args('yasoob', 'python', 'eggs', 'test')

# =============================================================================
# **kwargs 的用法
# =============================================================================
# 允许你将不定数量的键值对, 作为参数传递给一个函数。
# 如果你想要在一个函数里处理带名字的参数, 你应该使用**kwargs。
def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} == {1}".format(key, value))

greet_me(name="yasoob")
greet_me(name="yasoob",age=3) # 因为不定数量的，你也可以给两个，也能传进去

# =============================================================================
# #使用 *args 和 **kwargs 来调用函数
# =============================================================================
def test_args_kwargs(arg1, arg2, arg3):
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)
    
# 你可以使用*args或**kwargs来给这个小函数传递参数。
args = ("two", 3, 5)
test_args_kwargs(*args)

kwargs = {"arg3": 3, "arg2": "two", "arg1": 5}
test_args_kwargs(**kwargs)

# 标准参数与*args、**kwargs在使用时的顺序
some_func(fargs, *args, **kwargs) # 你可以在函数里里面同时使用这三种参数