# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:04:31 2019

@author: Administrator
"""

import PySimpleGUI as sg
import os
sg.change_look_and_feel('DarkAmber')   # Add a style

# All the stuff inside your window.
layout = [[sg.Text('填写基站信息')],
          [sg.Text('归属BSC: 1 or 2'), sg.InputText()],
          [sg.Text('输入基站IP: x.x.x.x'), sg.InputText()],
          [sg.Button('生成脚本'), sg.Button('退出')]]
# Create the Window
window = sg.Window('3G基站写IP脚本生成程序',layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, '退出'):  # if user closes window or clicks cancel
        break
    elif event in ('生成脚本'):  # if user closes window or clicks cancel
        if values[0] and values[1]:
            if int(values[0]) in [1, 2]:
                ip = [int(x) for x in values[1].split('.') if int(x) > 0 and int(x) < 255]
                if len(ip) != 4:
                    sg.Print('你输入的IP地址 {} 不正确！'.format(values[1]))
                else:
                    bts_ip1 = '0x0' + \
                        hex(ip[0]).replace('0x', '') if ip[0] < 16 else '0x' + \
                            hex(ip[0]).replace('0x', '')
                    bts_ip2 = '0' + hex(ip[1]).replace('0x',
                                                       '') if ip[1] < 16 else hex(ip[1]).replace('0x', '')
                    bts_ip3 = '0' + hex(ip[2]).replace('0x',
                                                       '') if ip[2] < 16 else hex(ip[2]).replace('0x', '')
                    bts_ip4 = '0' + hex(ip[3]).replace('0x',
                                                       '') if ip[3] < 16 else hex(ip[3]).replace('0x', '')
                    bts_ip = bts_ip1 + bts_ip2 + bts_ip3 + bts_ip4
                    mask = '0xffffffc0'
                    if ip[0] != 192:
                        gateway4 = '0' + hex(ip[3] // 64 * 64 + 1).replace('0x', '') if ip[3] // 64 * \
                            64 + 1 < 16 else hex(ip[3] // 64 * 64 + 1).replace('0x', '')
                    else:
                        gateway4 = '01' if ip[3] < 65 else '70'
                    gateway = bts_ip1 + bts_ip2 + bts_ip3 + gateway4
                    bsc_ip = '0x09440301' if int(values[0]) == 1 else '0x09440321'

                    # 将写IP脚本复制到windows剪贴板
                    write_ip_text = 'CfgDsmNetInfo {bts_ip},{mask},{gateway},{bsc_ip},65535'.format(
                        bts_ip=bts_ip,
                        mask=mask,
                        gateway=gateway,
                        bsc_ip=bsc_ip)
                    command = 'echo ' + write_ip_text.strip() + '| clip'
                    os.system(command)
                    # 使用dubug信息输出写IP脚本信息
                    sg.Print(
                        '你输入的信息为：' + '\n',
                        'BSC：{}'.format(values[0]) + '\n',
                        '基站IP地址：{}'.format(values[1]) + '\n',
                        '掩码：{}'.format('255.255.255.192') + '\n',
                        '网关：{}'.format(str(ip[0]) + '.' + str(ip[1]) + '.' +
                                       str(ip[2]) + '.' + str(ip[3] // 64 * 64 + 1)) + '\n',
                        '\n',
                        '写IP的脚本为：' + '\n',
                        '\n',
                        'CfgDsmNetInfo {bts_ip},{mask},{gateway},{bsc_ip},65535'.format(
                            bts_ip=bts_ip,
                            mask=mask,
                            gateway=gateway,
                            bsc_ip=bsc_ip) + '\n',
                        '\n',
                        '#' * 50 + '\n',
                        '\n',
                        '写IP脚本已复制到剪贴板，可以直接复制使用！')
            else:
                sg.Print('你输入的BSC号 {} 不正确！'.format(values[0]))
        else:
            sg.Print('你输入的信息不全！')
window.close()
