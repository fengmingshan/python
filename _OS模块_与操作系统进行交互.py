# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:34:03 2018
与操作系统进行交互：os 模块
@author: Administrator
"""
import os
import shutil


os.getcwd()     #得到当前工作目录，即当前Python脚本工作的目录路径
os.listdir()    #返回指定目录下的所有文件和目录名
os.path.isfile(r'D:\python\fms')    #检验给出的路径是否是一个文件
os.path.isdir(r'D:\python\fms')     #检验给出的路径是否是一个目录
os.path.isabs(r'D:\python\fms')     #判断是否是绝对路径
os.path.exists(r'D:\python\fms')    #检验给出的路径是否真地存
os.path.split(r'D:\python\fms\字符串截取.py')    #将一个文件名拆分成路径名和文件名
os.path.splitext(r'D:\python\fms\字符串截取.py')  #获取文件的扩展名
os.path.dirname(r'D:\python\fms\字符串截取.py')   #获取文件的路径名
os.path.basename(r'D:\python\fms\字符串截取.py')     #获取文件的文件名

os.system()     #运行shell命令

os.getenv()     #设置环境变量
os.putenv()     #设置环境变量
os.linesep  #给出当前平台使用的行终止符，Windows使用’\r\n’，Linux使用’\n’而Mac使用’\r’
os.name     #指示你正在使用的平台，对于Windows，它是’nt’，而对于Linux/Unix用户，它是’posix’
os.rename(old,new)  #重命名
os.exit()   #终止当前进程

# =============================================================================
# 文件操作
# =============================================================================
os.mknod('test.py')     #创建空文件
os.remove()     #用来删除一个文件
fp = open(r'D:\python\fms\test.py','w')   #直接打开一个文件,'w'表示如果不存在就创建它
'''
关于open 模式：
w 以写方式打开， 
a 以追加模式打开 (从 EOF 开始, 必要时创建新文件) 
r+ 以读写模式打开 
w+ 以读写模式打开 (参见 w ) 
a+ 以读写模式打开 (参见 a ) 
rb 以二进制读模式打开 
wb 以二进制写模式打开 (参见 w ) 
ab 以二进制追加模式打开 (参见 a ) 
rb+ 以二进制读写模式打开 (参见 r+ ) 
wb+ 以二进制读写模式打开 (参见 w+ ) 
ab+ 以二进制读写模式打开 (参见 a+ )
'''
os.stat(r'D:\python\fms\字符串截取.py')   #获取文件属性
os.chmod(r'D:\python\fms\字符串截取.py')     #修改文件权限与时间戳
os.path.getsize(r'D:\python\fms\字符串截取.py')   #获取文件大小

fp = open(r'D:\python\fms\test.py')
os.path.getsize(r'D:\python\fms\test.py') 
fp.read(100)  #制定长度读取文件，size为读取的长度[可选]，以byte为单位
fp.readline(100)   #读一行，如果定义了size，有可能返回的只是一行的一部分
fp.readlines(100)  #把文件每一行作为一个list的一个成员，并返回这个list。
#其实它的内部是通过循环调用readline()来实现的。
#如果提供size参数，size是表示读取内容的总长，也就是说可能只读到文件的一部分。

fp.write('fengmingshan')  #把str写到文件中，write()并不会在str后加上一个换行符
fp.writelines(seq)  #把seq的内容全部写到文件中(多行一次性写入)。这个函数也只是忠实地写入，不会在每行后面加上任何东西。

fp.close()  #关闭文件。

p.flush()   #把缓冲区的内容写入硬盘
fp.fileno()     #返回一个长整型的”文件标签“
fp.isatty()     #文件是否是一个终端设备文件（unix系统中的）
fp.tell()   #返回文件操作标记的当前位置，以文件的开头为原点
fp.next()   #返回下一行，并将文件操作标记位移到下一行。把一个file用于for … in file这样的语句时，就是调用next()函数来实现遍历的。
fp.seek(offset[,whence])    #将文件打操作标记移到offset的位置。这个offset一般是相对于文件的开头来计算的，一般为正数。但如果提供了whence参数就不一定了，whence可以为0表示从头开始计算，1表示以当前位置为原点计算。2表示以文件末尾为原点进行计算。需要注意，如果文件以a或a+的模式打开，每次进行写操作时，文件操作标记会自动返回到文件末尾。
fp.truncate([size])     #把文件裁成规定的大小，默认的是裁到当前文件操作标记的位置。如果size比文件的大小还要大，依据系统的不同可能是不改变文件，也可能是用0把文件补到相应的大小，也可能是以一些随机的内容加上去。

# =============================================================================
# 目录操作
# =============================================================================
os.makedirs(r'd：\python\test') 
#创建多级目录,注意改命令是创建在当前工作目录下，执行之后创建了一个D:\python\fms\d：\python\test
os.removedirs(r'd：\python\test')  
os.mkdir('test')    #创建单个目录,也是创建在当前工作目录下
os.removedirs(r'D:\python\fms\test')

shutil.copyfile('oldfile','newfile')    #复制文件，oldfile和newfile都只能是文件 
shutil.copy('oldfile','newfile')    #复制文件夹，oldfile只能是文件夹，newfile可以是文件，也可以是目标目录 
shutil.copytree('olddir','newdir')  #复制文件夹，olddir和newdir都只能是目录，且newdir必须不存在 
os.rename('oldname','newname')  #重命名文件（目录）文件或目录都是使用这条命令 
 
shutil.move(“oldpos”,”newpos”)  #移动文件（目录）
os.remove('file') #删除文件
#删除目录 
os.removedirs(r'D:\Game')  #删除整个目录,目录必须是空的，否则会报错 
os.rmdir('dir')     #只能删除空目录 
shutil.rmtree('dir')    #空目录、有内容的目录都可以删 

os.chdir(“path”)    #转换目录

# =============================================================================
# 文件、文件夹的移动、复制、删除、重命名
# =============================================================================

#导入shutil模块和os模块
import shutil

#复制单个文件
shutil.copy(r'C:\a\1.txt',r'C:\b')
#复制并重命名新文件
shutil.copy(r'C:\a\2.txt',r'C:\b\121.txt')
#复制整个目录(备份)
shutil.copytree(r'C:\a',r'C:\b\new_a')

#删除文件
os.unlink(r'C:\b\1.txt')
os.unlink(r'C:\b\121.txt')
#删除空文件夹
try:
    os.rmdir(r'C:\b\new_a')
except Exception as ex:
    print(r'错误信息：'+str(ex))     #提示：错误信息，目录不是空的

#删除文件夹及内容
shutil.rmtree(r'C:\b\new_a')

#移动文件
shutil.move(r'C:\a\1.txt',r'C:\b')
#移动文件夹
shutil.move(r'C:\a\c',r'C:\b')

#重命名文件
shutil.move(r'C:\a\2.txt',r'C:\a\new2.txt')
#重命名文件夹
shutil.move(r'C:\a\d',r'C:\a\new_d')