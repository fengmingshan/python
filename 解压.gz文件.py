# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:15:49 2020

@author: Administrator
"""

import gzip

def un_gz(file_name):
    # 获取文件的名称，去掉后缀名
    unzip_name = file_name.replace(".gz", "")
    # 开始解压
    g_file = gzip.GzipFile(file_name)
    #读取解压后的文件，并写入去掉后缀名的同名文件（即得到解压后的文件）
    with open(unzip_name, "wb+") as f:
        f.write(g_file.read())
        g_file.close()

un_gz(r'C:\Users\Administrator\Desktop\test\曲靖MR原始数据_1小时.csv.gz')

help(gzip.GzipFile)