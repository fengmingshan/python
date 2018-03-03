# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 17:20:26 2018
正则表达式处理中文
@author: Administrator
"""
import re  
  
msg = "这是一个例子"  
pat1 = "是"  
pat2 = "是(..){1,2}" # 两个..个中文字 ，{1,2}表示1-2个
pat3 = "是(..){1,2}?"  
  
res1 = re.search(pat1.encode('gbk'), msg.encode('gbk')) # 匹配出'是'  
if res1 is not None:  
    print(res1.group().decode('gbk'))  
  
res2 = re.search(pat2.encode('gbk'), msg.encode('gbk')) # 匹配出'是一个'  
if res2 is not None:  
    print(res2.group().decode('gbk'))  
  
res3 = re.search(pat3.encode('gbk'), msg.encode('gbk')) # 匹配出'是一'  
  
if res3 is not None:  
    print(res3.group().decode('gbk'))  
  
res4 = re.search(pat1.encode('utf'), msg.encode('utf'))  
  
if res4 is not None:  
    print(res4.group().decode('utf'))  
  
res5 = re.search('t.'.encode('utf'), 'this'.encode('utf'))  
  
if res5 is not None:  
    print(res5.group().decode('utf'))  
