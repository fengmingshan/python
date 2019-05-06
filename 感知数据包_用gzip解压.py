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

#unzip_file = gzip.open(file_path + "16进制.gz", 'rb') #打开压缩文件对象
file_content = open(file_path + "5月5号16进制.txt", 'rb').readlines()
for i in open(file_path + "5月5号16进制.txt", 'rb').readlines():
    unzip_file = BytesIO(i) #将读取的response信息作为stringIO方便后面作为文件写入
    if b'\x1f\x8b\x08\x00' in i :  
        print(i)

with open(file_path + "test1.xml","a") as file_out:#打开解压后内容保存的文件
    file_content = unzip_file.read()    #读取解压后文件内容
    file_out.write(file_content.decode('gbk','ignore'))

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
