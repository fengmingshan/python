# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:52:21 2019

@author: Administrator
"""

import os
import gzip
from io import BytesIO  

file_path = r'D:\test'+'\\'
out_path = r'D:\test'+'\\'
file_list = os.listdir(file_path)  #第一步取得文件夹里的所有文件名

file_content = open(file_path + "5月5号16进制.txt", 'rb').readlines()
file_lines = len(open(file_path + "5月5号16进制.txt", 'rb').readlines())

# 通过包头特征：\x1f\x8b\x08\x00 找gzip数据的包头所在的行
for i in range(0,file_lines,1):
    if b'\x1f\x8b\x08\x00' in file_content[i] :  
        packet_head = i

with gzip.open(file_path + "5月5号16进制.txt.gz", "wb") as f_out : #创建压缩文件对象    
    f_out.writelines(file_content[i:file_lines])

unzip_file =  gzip.open(file_path + "5月5号16进制.txt.gz", "rb")    
with open(file_path + "test1.xml","wb") as file_out: #打开解压后内容保存的文件
    file_content = unzip_file.read()    #读取解压后文件内容
    file_out.write(file_content.decode('gbk','ignore'))