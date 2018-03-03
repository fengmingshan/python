# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 08:35:39 2018

@author: Administrator
"""

import gzip
from io import StringIO

# gzip read a compress file 
with gzip.open(r'D:\2018年工作\2018年3月感知系统编程\file2.txt.gz','rb') as f:
    file_content = f.read()
    print(file_content)

# create a compressed GZIP file: 
content = b"Lots of content here"
with gzip.open('/home/joe/file.txt.gz', 'wb') as f:
    f.write(content)

# GZIP compress an existing file:
import shutil
with open(file, 'rb') as f_in:
    with gzip.open(r'D:\2018年工作\2018年3月感知系统编程\file2.txt.gz','wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# gzip压缩解压缩测试
def gzip_compress(raw_data):  
    buf = StringIO()  
    f = gzip.GzipFile(mode='wb', fileobj=buf)  
    try:  
        f.write(raw_data)  
    finally:  
        f.close()  
    return buf.getvalue()  

def gzip_uncompress(c_data):  
    buf = StringIO(c_data)  
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  

str2=b'This is Test String'

zip_data = gzip.compress(str2)
print('压缩后：',zip_data)

unzip_data=gzip.decompress(zip_data)
print('解压缩：',unzip_data)

# 压缩string
fp = open(r'D:\2018年工作\2018年3月感知系统编程\file2.txt') 
lines=fp.readlines
s_in = b"Lots of content here"
s_out = gzip.compress(s_in)

import binascii, os  
from io import StringIO  
  
def gzip_compress(raw_data):  
    buf = StringIO()  
    f = gzip.GzipFile(mode='wb', fileobj=buf)  
    try:  
        f.write(raw_data)  
    finally:  
        f.close()  
    return buf.getvalue()  
  
def gzip_uncompress(c_data):  
    buf = StringIO(c_data)  
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  
  
  
def compress_file(fn_in, fn_out):  
    f_in = open(fn_in, 'rb')  
    f_out = gzip.open(fn_out, 'wb')  
    f_out.writelines(f_in)  
    f_out.close()  
    f_in.close()  
  
def uncompress_file(fn_in, fn_out):  
    f_in = gzip.open(fn_in, 'rb')  
    f_out = open(fn_out, 'wb')  
    file_content = f_in.read()  
    f_out.write(file_content)  
    f_out.close()  
    f_in.close()  
  
  
if __name__ == '__main__':  
    in_data = 'hello, world!'  
    print in_data  
    out_data = gzip_compress(in_data)  
    print binascii.hexlify(out_data)  
  
    r_data = gzip_uncompress(out_data)  
    print r_data  
  
    raw_f = '/opt/log/raw/access.log_HLJYD-ICS-68_20150609040506.old'  
    #raw_f = '/home/taoyx/program_develop/python_dev/a.html';  
  
    gzip_f2 = '/opt/log/raw/access.log_HLJYD-ICS-68_20150609040506.gz'  