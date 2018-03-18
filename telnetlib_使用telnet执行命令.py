# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 09:44:04 2018

@author: Administrator
"""

import telnetlib  
from telnetlib import Telnet

username = 'qujing'
command='ping 6.49.20.239'

tn = telnetlib.Telnet(host = '6.48.255.24',port=23, timeout=10)

tn.read_until(b'login:',timeout=3)  
tn.write(b'qujing\n')  

tn.read_until(b'password:',timeout=3)  
tn.write(b'qjjk@2017\n' )  

tn.read_until(b'>')
tn.write(command.encode('ascii') + b'\n') 

tn.write(b'exit'+b'\n')  
content = tn.read_all().decode('ascii')


tn.close() 
    


 