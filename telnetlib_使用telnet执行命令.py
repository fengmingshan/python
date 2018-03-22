# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 09:44:04 2018

@author: Administrator
"""

import telnetlib  
from telnetlib import Telnet
import socket
import pandas as pd
import time

def test_socket_timeout():      #设置和测试socket_timeout的函数
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Default socket timeout: %s" %s.gettimeout())
    s.settimeout(100)
    print("Current socket timeout: %s" %s.gettimeout())

#test_socket_timeout()

path = 'd:\Eric'+'\\'
bts = 'bts_list.xls'

df_ip = pd.read_excel(path + bts , encoding='utf-8')
ip_list=list(df_ip['IP'])
command_list=list('ping '+x for x in ip_list)

tn = telnetlib.Telnet(host = '6.48.255.24',port=23, timeout=30)

tn.read_until(b'login:',timeout=5)  
tn.write(b'qujing\n')  

tn.read_until(b'password:',timeout=5)  
tn.write(b'qjjk@2017\n' )  

for command in command_list:   
    tn.write(command.encode('ascii') + b'\n') 

tn.write(b'exit'+b'\n')             
time.sleep(2)
content = tn.read_all().decode('ascii')
tn.close() 

F= open(path+'结果.txt','a',encoding='utf-8')
F.write(content)
F.close()

    


 