# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:02:42 2020

@author: Administrator
"""

import os
import IPy

om_ip = '9.80.20.76'
mask = 26

path = 'D:/'
os.chdir(path)

s1_ip = '.'.join(om_ip.split('.')[:-1]) + '.' + str(int(om_ip.split('.')[-1])-2**(32-mask))
s1_net = IPy.IP(s1_ip + '/'+str(mask),make_net=True)
om_net = IPy.IP(om_ip + '/'+str(mask),make_net=True)
s1_gateway = '.'.join(str(IPy.IP.net(s1_net)).split('.')[:-1]) + '.' +str(int(str(IPy.IP.net(s1_net)).split('.')[-1])+1)
om_gateway = '.'.join(str(IPy.IP.net(om_net)).split('.')[:-1]) + '.' +str(int(str(IPy.IP.net(om_net)).split('.')[-1])+1)

with open('./write_ip.mos', 'w') as f:
    f.writelines('lt all'+'\n')
    f.writelines('set InterfaceIPv4=TN_B_S1,AddressIPv4=1$ address {ip}/{mask}'.format(ip= s1_ip ,mask = mask)+'\n')
    f.writelines('set Router=S1,RouteTableIPv4Static=1,Dst=1,NextHop=1$ address {s1_gateway}'.format(s1_gateway= s1_gateway)+'\n')
    f.writelines('set InterfaceIPv4=TN_B_OAM,AddressIPv4=1$ address {ip}/{mask}'.format(ip= om_ip ,mask = mask)+'\n')
    f.writelines('set Router=vr_OAM,RouteTableIPv4Static=1,Dst=1,NextHop=1$ address {om_gateway}'.format(om_gateway= om_gateway)+'\n')

