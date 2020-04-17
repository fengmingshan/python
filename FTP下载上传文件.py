# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:25:22 2020

@author: Administrator
"""

import os
from ftplib import FTP
import time
import tarfile

#连接ftp
def ftpconnect(host,port, username, password):
    ftp = FTP()
    # 打开调试级别2，显示详细信息
    # ftp.set_debuglevel(2)
    ftp.connect(host, port)
    ftp.login(username, password)
    return ftp


#从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
    # 设置的缓冲区大小
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)# 参数为0，关闭调试模式
    fp.close()


#从本地上传文件到ftp
def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    ftp = ftpconnect("135.32.1.36", 2121,"ftpuser", "ftpoptr")
    print(ftp.getwelcome())# 打印出欢迎信息
    # 获取当前路径
    pwd_path = ftp.pwd()
    print("FTP当前路径:", pwd_path)
    # 设置FTP当前操作的路径
    ftp.cwd('/MR报表/日报表')
    # 返回一个文件名列表
    filename_list = ftp.nlst()
    print(filename_list)

    downloadfile(ftp, "/MR报表/日报表/", r"d:\Test\text.csv")
    # 上传文件，第一个是要上传到ftp服务器路径下的文件，第二个是本地要上传的的路径文件
#    uploadfile(ftp, '/upload/1.txt', "C:/Users/Administrator/Desktop/1.txt")
    # ftp.close() #关闭ftp
