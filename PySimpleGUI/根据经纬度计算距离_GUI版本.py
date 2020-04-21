# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:15:30 2019

@author: Administrator
"""

import os
import pandas as pd
from tqdm import tqdm,trange
import time
from datetime import datetime
from math import sin
from math import cos
from math import tan
from math import asin
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
from math import sqrt
from math import ceil
import PySimpleGUI as sg

# =============================================================================
# 定义GUI界面
# =============================================================================
sg.change_look_and_feel('DarkAmber')   # Add a style
# 定义GUI窗体布局
layout = layout = [[sg.Text('打开源小区文件')],
                   [sg.Input('d:/'),
                    sg.FilesBrowse(file_types=(('Excel2007', '*.xlsx'), ('Excel2003', '*.xls'),), initial_folder='d:/')],
                   [sg.Text('打开目标小区文件')],
                   [sg.Input('d:/'),
                    sg.FilesBrowse(file_types=(('Excel2007', '*.xlsx'), ('Excel2003', '*.xls'),), initial_folder='d:/')],
                   [sg.Text('设置最大相邻距离'),
                    sg.Input(default_text='整数，单位：米', size=(25, 1),do_not_clear=True)],
                   [sg.Button('开始计算'),
                    sg.Button('退出')]]
# 新建窗体，引用之前定义好的布局
window = sg.Window('计算基站距离小程序', layout)


def calc_Distance(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)]) # 经纬度转换成弧度
    dlon = lon2-lon1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance,0)
    return distance


while True:
    event, values = window.read()
    if event in (None, '退出'):  # if user closes window or clicks cancel
        break
    elif event in ('开始计算'):
        if os.path.isfile(values[0]) and os.path.isfile(values[1]) and values[2].isdigit():
            sg.Print('你选择的源小区文件是{}。'.format(values[0]))
            sg.Print('你选择的目标小区文件是{}。'.format(values[1]))
            sg.Print('最大相邻距离设置为{}。'.format(values[2]))
            sg.Print('开始计算距离。'.center(60,'#'),'\n')

            source_cell_info = values[0]
            destination_cell_info = values[1]

            path_list = source_cell_info.split('/')
            data_path = '/'.join(path_list[:-1])
            os.chdir(data_path)
            max_distance = int(values[2])

            df_source_cell = pd.read_excel(source_cell_info)
            df_source_cell.columns=['name','eNodeB','lon','lat']
            df_source_cell['lon'] = df_source_cell['lon'].map(lambda x: round(x, 5))
            df_source_cell['lat'] = df_source_cell['lat'].map(lambda x: round(x, 5))

            df_destination_cell = pd.read_excel(destination_cell_info)
            df_destination_cell.columns=['name','eNodeB','lon','lat']
            df_destination_cell['lon'] = df_destination_cell['lon'].map(lambda x: round(x, 5))
            df_destination_cell['lat'] = df_destination_cell['lat'].map(lambda x: round(x, 5))

            df_res = pd.DataFrame()
            df_res['s_eNodeB'] = tqdm([x for x in df_source_cell['eNodeB'] for y in df_destination_cell['eNodeB']])
            df_res['s_name'] = tqdm([x for x in df_source_cell['name'] for y in df_destination_cell['name']])
            df_res['s_lon'] = tqdm([x for x in df_source_cell['lon'] for y in df_destination_cell['lon']])
            df_res['s_lat'] = tqdm([x for x in df_source_cell['lat'] for y in df_destination_cell['lat']])
            df_res['des_eNodeB'] = tqdm([y for x in df_source_cell['eNodeB'] for y in df_destination_cell['eNodeB']])
            df_res['des_name'] = tqdm([y for x in df_source_cell['name'] for y in df_destination_cell['name']])
            df_res['des_lon'] = tqdm([y for x in df_source_cell['lon'] for y in df_destination_cell['lon']])
            df_res['des_lat'] = tqdm([y for x in df_source_cell['lat'] for y in df_destination_cell['lat']])
            df_res['distance'] = tqdm([calc_Distance(a, b, c, d) for a, b, c, d in zip(
            df_res['s_lon'], df_res['s_lat'], df_res['des_lon'], df_res['des_lat'])])
            df_res = df_res[['s_name', 's_eNodeB', 's_lon', 's_lat', 'des_name',
                             'des_eNodeB', 'des_lon', 'des_lat', 'distance']]
            df_res['distance'] = df_res['distance'].map(lambda x: ceil(x))
            df_res = df_res[df_res['distance'] < max_distance]
            df_min_distance = df_res.groupby(['s_eNodeB', 's_name', 's_lon', 's_lat'], as_index=False)['distance'].agg(min)
            df_min_distance = df_min_distance[df_min_distance['distance'] > max_distance]
            with open('距离计算结果.csv', 'w', newline = '') as writer:
                df_min_distance.to_csv(writer, '最小距离', index=False)
                df_res.to_csv(writer, index=False)
            sg.Print('\n' + '结果已输出到：{path}，请到该目录查看！'.format(path=os.getcwd().replace('\\\\', '\\') + '\\'))
            time.sleep(6)
            os.startfile(data_path)
        else:
            sg.Print('你的输入信息不全，请检查源小区、目标小区及最大相邻距离是否都已经设置！')

