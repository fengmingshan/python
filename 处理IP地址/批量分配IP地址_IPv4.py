# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:51:11 2019

@author: fengmingshan
"""


from IPy import IP
import pandas as pd

def get_ip_list(begin_ip, count, netmask):
    ip_list = '' #用来存放生成的IP地址
    begin_ip = IP(begin_ip)
    ip_list += str(begin_ip) + '\n' #将第一个地址放入ip_列表中
    if begin_ip.version() == 4:
        for i in range(count):
            ip = IP(begin_ip)
            new_ip = IP(ip.ip + 2 ** (32 - netmask))
            begin_ip =  str(new_ip)
            ip_list += begin_ip + '\n'
    else:
        for i in range(count):
            ipv6 = IP(begin_ip)
            new_ipv6 = IP(ipv6.ip + 2 ** (128 - netmask))
            begin_ip =  str(new_ipv6)
            ip_list += begin_ip + '\n'
    return ip_list

if __name__ == "__main__":
    num = 20
    mask = 28
    start_ip = '53.3.16.144'
    ipv4_list  = get_ip_list(begin_ip = start_ip, count=num-1, netmask=mask)
    print('批量分配业务IPv4地址:')
    print('============================')
    print(ipv4_list)

    ip_list = ipv4_list.strip().split('\n')
    gateway = ['.'.join(x.split('.')[:-1])+'.'+str(int(x.split('.')[-1])+1) for x in ip_list]
    ip_num = [IP(x+'/{}'.format(mask)).len()-3 for x in ip_list]
    ip_add_begin = [str(IP(x+'/{}'.format(mask))[2]) for x in ip_list]
    ip_add_end =  [str(IP(x+'/{}'.format(mask))[-2]) for x in ip_list]

    df_ip = pd.DataFrame({
            'no':range(len(ip_list)),
            'IP地址段':ip_list,
            '网关':gateway,
            '掩码':mask,
            '数量':ip_num,
            '起始地址':ip_add_begin,
            '终止地址':ip_add_end,
            '区县':'',
            '厂家':'',
            '备注':'',
            })
    with open(r'C:\Users\Administrator\Desktop\IPv4_address.csv','w',newline = '') as f:
        df_ip.to_csv(f,index = False)
#    ipv6_list2  = get_ip_list(begin_ip = 'FD00:0:2e3f::', count=10, netmask=127)
#    print('批量分配互联IPv6地址:')
#    print('============================')
#    print(ipv6_list2)
#
#    ip_list = get_ip_list(begin_ip='192.168.1.0', count=10,netmask=24)
#    print('批量分配业务IPv4地址:')
#    print('============================')
#    print(ip_list)
#
#    ip_list2 = get_ip_list(begin_ip='192.168.2.0', count = 10, netmask=30)
#    print('批量分配互联IPv4地:')
#    print('============================')
#    print(ip_list2)