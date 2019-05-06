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