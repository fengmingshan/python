# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:05:37 2018

@author: Administrator
"""
import telnetlib  
from telnetlib import Telnet
import socket


path=r'd:\Eric' + '\\'
command_file = open(path + 'command.txt','r',encoding='utf-8')
command_list = command_file.readlines()

tn = telnetlib.Telnet(host='6.48.255.24',port=23, timeout=10)     # 连接telnet服务器 
tn.set_debuglevel(2)   
tn.read_until(b'login:',timeout=5)   # 登录
tn.write(b'qujing\n')      
tn.read_until(b'password:',timeout=5)  # 登录
tn.write(b'qjjk@2017\n' )
for i in range(0,len(command_list),1):
        tn.write(command_list[i].encode('ascii') + b'\n')   # 输入ping命令 
        tn.read_until(b'>')
    except socket.timeout:
        pass
        
tn.write(b'exit'+b'\n')       # 退出telnet服务器     
time.sleep(2)    
#content = tn.set_debuglevel(10000)
try:
    content = tn.read_all().decode('ascii')  # 保存测试结果   
except socket.timeout:
    pass

#content = tn.read_very_eager().decode('ascii')  # 保存测试结果 

tn.close()      

