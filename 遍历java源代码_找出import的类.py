# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:23:37 2019

@author: Administrator
"""
import os

data_path = r'd:\test\源文件中的所有类'+'\\'
out_path = r'd:\test'+'\\'

file_list = []
for root, dirs, files in os.walk(data_path):
    for name in files:
        file_list.append(os.path.join(root, name))

java_file = [x for x in file_list if '.java' in x]

with open(out_path + 'java文件列表.txt' ,'w') as writer:
    for line in java_file:
        writer.writelines(line + '\n') 

line_list = []    
for file_name in java_file:
    file_content = open(file_name,encoding = 'utf-8').readlines()
    for line in file_content:
        if  'import ' in line: 
            line_list.append(line.replace('\n','') + ' ' + file_name + '\n')

with open(out_path + 'import库列表.txt' ,'w') as writer:
    for line in line_list:
        writer.writelines(line)
            
            