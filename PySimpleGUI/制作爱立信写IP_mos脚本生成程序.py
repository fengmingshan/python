# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:04:31 2019

@author: Administrator
"""

import PySimpleGUI as sg
import os
import IPy

path = 'D:/'
os.chdir(path)

sg.change_look_and_feel('DarkAmber')   # Add a style

# All the stuff inside your window.
layout = [[sg.Text('爱立信基站IP: x.x.x.x'), sg.InputText()],
          [sg.Text('掩码: 两位数字'), sg.InputText()],
          [sg.Button('生成脚本'), sg.Button('退出')]]
# Create the Window
window = sg.Window('爱立信基站写IP_mos脚本生成程序',layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, '退出'):  # if user closes window or clicks cancel
        break
    elif event in ('生成脚本'):  # if user closes window or clicks cancel
        if values[0] and values[1]:
            om_ip = values[0]
            mask = int(values[1])

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


            # 使用dubug信息输出写IP脚本信息
            sg.Print(
                '你输入的信息为：' + '\n',
                '爱立信基站IP{}'.format(values[0]) + '\n',
                '掩码：{}'.format(values[1]) + '\n',
                '写IP脚本已输出到"D:/write_ip.mos"！')
        else:
            sg.Print('你输入的信息不全！')
window.close()
