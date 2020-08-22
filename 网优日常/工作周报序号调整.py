# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:25:30 2020

@author: Administrator
"""

import os


path = r'C:\Users\Administrator\Desktop'
os.chdir(path)
with open('第34周工作周报.txt') as f:
    content = f.read()
    graphs = content.split('\n\n')
    graph1 = graphs[0].split('\n')
    graph2 = graphs[1].split('\n')
    graph3 = graphs[2].split('\n')
    graph1 = [x.split('.')[1] for x in graph1 if len(x.split('.'))>1]
    graph2 = [x.split('.')[1] for x in graph2 if len(x.split('.'))>1]
    graph3 = [x.split('.')[1] for x in graph3 if len(x.split('.'))>1]

with open('工作周报_调整格式.txt','w') as f:
    f.writelines('无线中心全部工作汇总：')
    f.writelines('\n')
    f.writelines('\n')
    for num,line in enumerate(graph1):
        f.writelines(str(num+1)+'.')
        f.writelines(line)
        f.writelines('\n')
    f.writelines('\n')
    f.writelines('一、无线网维护方面：')
    f.writelines('\n')
    f.writelines('\n')
    for num,line in enumerate(graph2):
        f.writelines(str(num+1)+'.')
        f.writelines(line)
        f.writelines('\n')
    f.writelines('\n')
    f.writelines('二、无线网优化方面：')
    f.writelines('\n')
    f.writelines('\n')
    for num,line in enumerate(graph3):
        f.writelines(str(num+1)+'.')
        f.writelines(line)
        f.writelines('\n')
