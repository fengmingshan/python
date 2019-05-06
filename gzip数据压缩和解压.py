# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:59:50 2018

@author: Administrator
"""

import gzip

file_path = r'D:\test'+'\\'

# 使用gzip模块完成对文件的压缩。

with open(file_path + "data.txt", "rb")  as f_in : #打开文件
    with gzip.open(file_path + "data.txt.gz", "wb") as f_out : #创建压缩文件对象    
        f_out.writelines(f_in)
    


# 使用gzip模块完成对文件的解压。

with gzip.open(file_path + "data.txt.gz", "rb") as f_zip : #创建压缩文件对象
    file_content = f_zip.read()    #读取解压后文件内容
    print(file_content) #打印读取内容

    with open(file_path + "data_unzip.txt", "a")  as f_out : #打开文件            
        f_out.write(file_content.decode("utf-8")) #写入新文件当中
        
