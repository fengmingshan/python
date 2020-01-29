# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 16:25:48 2018

@author: Administrator
"""


data_path = r'd:\_LAC修改脚本' + '\\'
file = 'BSC2_修改reg反馈.txt'
with open(data_path + file,encoding = 'gbk') as f:
    line_list = f.readlines()
    success_list = []  
    fault_list = []
    for i in range(0,len(line_list)-4):
        if 'No' in line_list[i] and 'OK' in line_list[i+4]:
            success_list.append(line_list[i])
        elif 'No' in line_list[i] and 'OK' not in line_list[i+4]: 
            fault_list.append(line_list[i])            

with open(data_path + '执行成功.txt','w') as f:
    for line in success_list:
        f.write(line)

with open(data_path + '执行失败.txt','w') as f:
    for line in fault_list:
        f.write(line)


            