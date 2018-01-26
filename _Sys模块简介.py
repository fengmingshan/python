# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:14:47 2018
###sys模块简介
@author: Administrator
"""

import sys
sys.argv    #显示传入的参数：



%%writefile print_args.py  #写入一个程序
import sys
print(sys.argv)

%run print_args.py 1 foo  #运行这个程序


import os              
os.remove('print_args.py')  #删除这个程序

#sys.exc_info() 可以显示 Exception 的信息，返回一个 (type, value, traceback) 组成的三元组，
#可以与 try/catch 块一起使用：
#sys.exc_clear() 用于清除所有的异常消息。

try:
    x = 1/0
except Exception:
    print(sys.exc_info()) 

#标准输入输出流  
#sys.stdin
#sys.stdout
#sys.stderr

sys.exit(arg=0)  #用于退出 Python。0 或者 None 表示正常退出，其他值表示异常

sys.path    #表示Python搜索模块的路径和查找顺序：

sys.platform    #显示当前操作系统信息：

sys.getwindowsversion()     #返回 Windows 操作系统的版本：   

sys.version     #Python 版本信息

sys.version_info    #Python 版本信息


