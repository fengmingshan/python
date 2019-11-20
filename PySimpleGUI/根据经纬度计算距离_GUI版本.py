# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:15:30 2019

@author: Administrator
"""

import os
import pandas as pd
import time
from datetime import datetime
from math import sin
from math import cos
from math import tan
from math import acos
from math import degrees
from math import radians
from math import atan2
from math import atan
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


def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
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
            df_source_cell['lon'] = df_source_cell['lon'].map(lambda x: round(x, 5))
            df_source_cell['lat'] = df_source_cell['lat'].map(lambda x: round(x, 5))

            df_destination_cell = pd.read_excel(destination_cell_info)
            df_destination_cell['lon'] = df_destination_cell['lon'].map(lambda x: round(x, 5))
            df_destination_cell['lat'] = df_destination_cell['lat'].map(lambda x: round(x, 5))
            df_destination_cell.rename(
                columns={
                    'name': 'des_name',
                    'eNodeB': 'des_eNodeB',
                    'lon': 'des_lon',
                    'lat': 'des_lat'},
                inplace=True)

            list_res = []
            start_time = datetime.now()
            for i in range(len(df_source_cell)):
                df_tmp = df_destination_cell[(df_destination_cell['des_lon'] != df_source_cell.loc[i, 'lon']) & (
                    df_destination_cell['des_lat'] != df_source_cell.loc[i, 'lat'])]
                df_tmp['s_name'] = df_source_cell.loc[i, 'name']
                df_tmp['s_eNodeB'] = df_source_cell.loc[i, 'eNodeB']
                df_tmp['s_lon'] = df_source_cell.loc[i, 'lon']
                df_tmp['s_lat'] = df_source_cell.loc[i, 'lat']
                df_tmp['distance'] = df_tmp.apply(
                    lambda x: getDistance(
                        x.s_lat,
                        x.s_lon,
                        x.des_lat,
                        x.des_lon),
                    axis=1)
                df_tmp = df_tmp[df_tmp['distance'] <= max_distance]
                list_res.append(df_tmp)
                if i > 0 and i % 100 == 0:
                    bantch_time = datetime.now()
                    delta_time = (bantch_time - start_time).seconds
                    sg.Print('\n', '  Part Report  '.center(60, '#'))
                    sg.Print('Total {total} cells,finished {finish} cells, remain {remain} cells！'.format(
                        total=len(df_source_cell), finish=i, remain=len(df_source_cell) - i))
                    sg.Print('Take {seconds} seconds!'.format(seconds=delta_time))
                elif i == len(df_source_cell) - 1:
                    total_time = datetime.now()
                    delta_time = (total_time - start_time).seconds
                    sg.Print('\n', '  Global Report  '.center(60, '#'))
                    sg.Print('ALL {total} cells finished !'.format(total=len(df_source_cell)))
                    sg.Print('Total take {seconds} seconds!'.format(seconds=delta_time))

            df_res = pd.concat(list_res, axis=0)
            df_res = df_res[['s_name', 's_eNodeB', 's_lon', 's_lat', 'des_name',
                             'des_eNodeB', 'des_lon', 'des_lat', 'distance']]
            df_res['distance'] = df_res['distance'].map(lambda x: ceil(x))
            with open('距离计算结果.csv', 'w') as writer:
                df_res.to_csv(writer, index=False)
            sg.Print('\n' + '结果已输出到：{path}，请到该目录查看！'.format(path=os.getcwd().replace('\\\\', '\\') + '\\'))
            os.startfile(data_path)
        else:
            sg.Print('你的输入信息不全，请检查源小区、目标小区及最大相邻距离是否都已经设置！')

