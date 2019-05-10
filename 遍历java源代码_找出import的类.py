# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:23:37 2019

@author: Administrator
"""
import os

data_path = r'd:\test\省级插件源代码'+'\\'
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
file_name_set = set() 

for file_name in java_file:
    with open(file_name,encoding = 'utf-8') as file_content:
        for line in file_content.readlines():
            if  'curl_setopt' in line: 
                line_list.append(line.replace('\n','') + ' ' + file_name + '\n')
                file_name_set.update(file_name)
                
with open(out_path + '插件源代码包含_' + 'curl_setopt'  + '.txt' ,'w') as writer:
    for line in line_list:
        writer.writelines(line)

with open(out_path + '插件源代码包含_' + 'curl_setopt'  + '的文件名.txt' ,'w') as writer:
    file_name_set = list(file_name_set)
    for line in file_name_set:
        writer.writelines(line)

            
            