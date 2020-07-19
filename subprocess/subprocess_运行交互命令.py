# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:50:32 2020

@author: Administrator
"""
import subprocess

s = subprocess.Popen("python", stdout=subprocess.PIPE, stdin=subprocess.PIPE)
s.stdin.write(b"import os\n")
s.stdin.write(b"print(os.environ)")
s.stdin.close()
out = s.stdout.read().decode("GBK")
print(out)
s.stdout.close()

# 用文本写入命令
'''
111.txt的内容是：
import os
print(os.getcwd())
'''

f = open(r"D:\_python\python\subprocess\111.txt", "r+")
s = subprocess.Popen("python",stdout=subprocess.PIPE, stdin=f, shell=True)
out = s.stdout.read().decode("gbk")
s.stdout.close()
print(out)

cmd = 'mysql -u root  -p'
f = open(r"D:\_python\python\subprocess\passwd.txt", "r+")
s = subprocess.Popen([cmd,'a123456/n'],stdout=subprocess.PIPE,stderr = subprocess.PIPE, shell=True)
err = s.stderr.read().decode("gbk")
s.stderr.close()
print(err)
