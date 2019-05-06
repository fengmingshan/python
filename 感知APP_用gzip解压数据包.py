# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:52:21 2019

@author: Administrator
"""

import os
import gzip
from io import BytesIO  
from io import StringIO 

file_path = r'D:\test'+'\\'
out_path = r'D:\test'+'\\'
file_list = os.listdir(file_path)  #第一步取得文件夹里的所有文件名

# gzip 解压函数
def gzip_uncompress(c_data):  
    '''定义gzip解压函数'''
    buf =BytesIO(c_data)   # 通过IO模块的BytesIO函数将Bytes数据输入，这里也可以改成StringIO，根据你输入的数据决定
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  


file_content = open(file_path + "5月5号16进制.dat", 'rb').readlines()
file_lines = len(open(file_path + "5月5号16进制.dat", 'rb').readlines())

# 通过包头特征：\x1f\x8b\x08\x00 找gzip数据的包头所在的行
for i in range(0,file_lines,1):
    if b'\x1f\x8b\x08\x00' in file_content[i] :  
        packet_head = i

zip_content = b''
for i in range(packet_head,file_lines,1):
    zip_content = zip_content + file_content[i]
    
unzip_file =  gzip_uncompress(zip_content)    

with open(file_path + "5月5号_解.xml",'wb') as file_out: #打开解压后内容保存的文件
    file_out.write(unzip_file)

