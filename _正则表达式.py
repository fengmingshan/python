# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 17:20:26 2018
正则表达式处理中文
@author: Administrator
"""
import re  
#==============================================================================
#  正则表达式入门-1
#==============================================================================
key = r"<html><body><h1>hello world<h1></body></html>" # 这是要匹配的文本
p1 = r"(?<=<h1>).+?(?=<h1>)" # 这是我们写的正则表达式规则，你现在可以不理解啥意思
pattern1 = re.compile(p1) # 我们在编译这段正则表达式
matcher1 = re.search(pattern1,key) # 在源文本中搜索符合正则表达式的部分
if matcher1: # 如果匹配成功
    print(matcher1.group()) # 打印出来

#==============================================================================
# 正则表达式入门-2
#==============================================================================
key = r"javapythonhtmlvhdl" # 这是源文本
p1 = r"python" # 这是我们写的正则表达式
pattern1 = re.compile(p1) # 编译
matcher1 = re.search(pattern1,key) # 是查询
if matcher1: # 如果匹配成功
    print(matcher1.group()) #打印出来



#==============================================================================
# 正则表达式匹配中文的例子   
#==============================================================================
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
