# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 07:21:37 2020

@author: Administrator
"""

import IPy


# 根据IP和掩码查询网关
om_ip = '9.68.232.194'
mask = 26

s1_ip = '.'.join(om_ip.split('.')[:-1]) + '.' + str(int(om_ip.split('.')[-1])-2**(32-mask))
s1_net = IPy.IP(s1_ip + '/'+str(mask),make_net=True)
om_net = IPy.IP(om_ip + '/'+str(mask),make_net=True)
s1_gateway = '.'.join(str(IPy.IP.net(s1_net)).split('.')[:-1]) + '.' +str(int(str(IPy.IP.net(s1_net)).split('.')[-1])+1)
om_gateway = '.'.join(str(IPy.IP.net(om_net)).split('.')[:-1]) + '.' +str(int(str(IPy.IP.net(om_net)).split('.')[-1])+1)

s1_net
om_net
s1_gateway
om_gateway


# 查看网段中包含哪些IP地址
from IPy import IP  # 导入模块
net_segment = IP('10.0.0.16/28')  # 将这个网段的IP赋值给一个变量，/28是C类IP地址的子网划分

print(net_segment.len())  # 查看变量中的具体数量

for i in jier:  # 遍历变量中的每一条信息
    print(i)  # 打印出来你遍历到的信息

str(jier[0])
str(jier[-1])


net_segmentv6 = IP('240e:184:c00c::0/120')  # 将这个网段的IP赋值给一个变量，/28是C类IP地址的子网划分

print(net_segmentv6.len())  # 查看变量中的具体数量
