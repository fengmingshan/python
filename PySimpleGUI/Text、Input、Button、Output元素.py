# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-11-19 19:22:07
# @Last Modified by:   Administrator
# @Last Modified time: 2019-11-20 17:20:08

import os
import pandas as pd
import time
from datetime import datetime
import PySimpleGUI as sg

# =============================================================================
# 定义GUI界面
# =============================================================================
sg.change_look_and_feel('DarkAmber')   # Add a style
# 定义GUI窗体布局
layout = layout = [[sg.Text('文件0')],
                   [sg.Input('d:/')],
                   [sg.Text('文件1')],
                   [sg.Input('d:/')],
                   [sg.Text('参数2'),
                    sg.Input(default_text='整数，单位：米', size=(25, 1),do_not_clear=True)],
                   [sg.Onput(size=(60,10)],
                   [sg.Button('开始'),
                    sg.Button('打印参数'),
                    sg.Button('退出')]]
# 新建窗体，引用之前定义好的布局
window = sg.Window('计算基站距离小程序', layout)

while True:
    event, values = window.read()
    if event in (None, '退出'):  # if user closes window or clicks cancel
        break
    elif event in ('开始'):
        if os.path.isfile(values[0]) and os.path.isfile(values[1]) and values[2].isdigit():
            print('你选择的源小区文件是{}。'.format(values[0]))
            print('你选择的目标小区文件是{}。'.format(values[1]))
            print('最大相邻距离设置为{}。'.format(values[2]))
            print('开始计算距离。'.center(60,'#'),'\n')
            for i in range(10):
            	print('第{}次运行，还有{}次。'.format(i+1,9-i))
        if not path.isfile(values[0]):
        	print('文件0设置错误，必须为文件！')
        if not path.isfile(values[1]):
        	print('文件1设置错误，必须为文件！！')
    	if not values[2].isdigit():
    		print('参数2设置错误，必须为整数！')
        else:
            print('你的输入信息不全，请检查源小区、目标小区及最大相邻距离是否都已经设置！')

