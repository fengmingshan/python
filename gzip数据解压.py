# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:59:50 2018

@author: Administrator
"""

import os
import gzip
from io import BytesIO  

file_path = r'D:\test'+'\\'
out_path = r'D:\test'+'\\'
file_list = os.listdir(file_path)  #第一步取得文件夹里的所有文件名

#unzip_file = gzip.open(file_path + "16进制.gz", 'rb') #打开压缩文件对象
file_content = open(file_path + "5月5号16进制.txt", 'rb').readlines()
file_lines = len(open(file_path + "5月5号16进制.txt", 'rb').readlines())

for i in range(0,file_lines,1):
    if b'\x1f\x8b\x08\x00' in file_content[i] :  
        packet_head = i
        
with open(file_path + "test1.xml","a") as file_out:#打开解压后内容保存的文件
    file_content = unzip_file.read()    #读取解压后文件内容
    file_out.write(file_content.decode('gbk','ignore'))

