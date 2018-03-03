# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:21:03 2018

@author: Administrator
"""

import os  
import shutil  
  
# 一. 路径操作：判断、获取和删除  
  
#1. 得到当前工作目录，即当前Python脚本工作的目录路径: os.getcwd()  
#print: currentpath:  f:\LearnPython  
currentpath = os.getcwd()  
print "currentpath: ",currentpath  
#2. 返回指定目录下的所有文件和目录名:os.listdir()  
#print:os.listdir():  ['test.txt', 'testRW.py', 'test1.txt', 'cmd.py', 'rwfile.py', 'downloadfile.py', 'date.py', 'time.py', 'datetime.py', 'file.py']  
print "os.listdir(): ",os.listdir('f:\LearnPython')  
  
path = "F:\mmmmmmmmm\debug_taobao_200003@taobao_android1.6_3.2.1.apk"  
#3. 判断给出的路径是否真地存:os.path.exists()  
if os.path.exists(path):  
    #删除一个文件:os.remove()  
    os.remove(path)  
else:  
    print path,"not exist"  
  
#4. 删除多个目录：os.removedirs（“c：\python”）  
#它只能删除空目录，如果目录里面有内容将不会被删除  
if os.path.exists("d:/woqu"):  
    os.removedirs("d:/woqu")  
else:  
    os.mkdir("d:/woqu")  
    os.removedirs("d:/woqu")  
  
#5. 判断给出的路径是否是一个文件：os.path.isfile()  
#print: True  
print os.path.isfile("D:\hello\json.txt")  
#6. 判断给出的路径是否是一个目录：os.path.isdir()  
#print: True  
print os.path.isdir("D:\hello")  
#7. 判断是否是绝对路径：os.path.isabs()  
#print: True  
print os.path.isabs("D:\hello")  
#  判断是否是链接  
print os.path.islink('http://www.baidu.com')  
#8. 返回一个路径的目录名和文件名:os.path.split()       
#eg os.path.split('/home/swaroop/byte/code/poem.txt') 结果：('/home/swaroop/byte/code', 'poem.txt')   
#print: ('D:\\hello', 'json.txt')  
print os.path.split("D:\hello\json.txt")  
#9. 分离扩展名：os.path.splitext()  
#print:('D:\\hello\\json', '.txt')  
print os.path.splitext("D:\hello\json.txt")  
#10. 获取路径名：os.path.dirname()  
#print: 'D:\\hello'  
print os.path.dirname("D:\hello\json.txt")  
#11. 获取文件名：os.path.basename()  
#print: 'json.txt'  
print os.path.basename("D:\hello\json.txt")  
  
  
#13. 指示你正在使用的平台：os.name       对于Windows，它是'nt'，而对于Linux/Unix用户，它是'posix'  
print "os.name: ",os.name  
  
#14. linex 下的命令  
if os.name == 'posix':  
    #读取和设置环境变量:os.getenv() 与os.putenv()  
    home_path = os.environ['HOME']  
    home_path = os.getenv('HOME')  #读取环境变量　  
elif os.name == 'nt':  
    home_path = 'd:'   
    print 'home_path: ',home_path  
  
#15. 给出当前平台使用的行终止符:os.linesep    Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'  
print(os.linesep)  
  
#16. 应为windows和linux的路径有点点不一样，windows是用 \\ 来分割的，linux是用 / 来分隔，  
#而用os.sep 会自动根据系统选择用哪个分隔符。  
print(os.sep)  
  
#17. 重命名：os.rename（old， new）  
#先进入目录  
os.chdir("d:\\hello")  
print os.getcwd()   
#18. 再重命名  
os.rename("1.txt", "11.txt")  
#19. 创建多级目录：os.makedirs（“c：\python\test”）  
os.makedirs('d:\h\e\l\l\o')  
#20. 创建单个目录：os.mkdir（“test”）  
os.mkdir('d:\f')  
#21. 获取文件属性：os.stat（file）  
#print: nt.stat_result(st_mode=33206, st_ino=0L, st_dev=0, st_nlink=0, st_uid=0, st_gid=0, st_size=497L, st_atime=1346688000L, st_mtime=1346748054L, st_ctime=1346748052L)  
print os.stat('d:\hello\json.txt')  
#22. 修改文件权限与时间戳：os.chmod（path,mode）  
#这里有介绍：http://blog.csdn.net/wirelessqa/article/details/7974477  
#23. 终止当前进程：os.exit（）  
#24. 获取文件大小：os.path.getsize（filename）  
print os.path.getsize('d:/hello/json.txt')  