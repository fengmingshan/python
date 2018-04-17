# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 08:47:33 2018
for循环运用基础
@author: Administrator
"""

#这里有一个目录f:\test里面有5个txt文件，使用循环打开每一个文件并读取指定的内容,然后汇总写出到一个文件
import os

File=os.listdir(r'D:\test')  #第一步取得文件夹里的所有文件名
D=r'D:\test'
print(File)    #取出之后可以通过print看一下，File是一个5个元素的list


#依次打开5个文件就要用到循环
#有两种方法实现
#第1种：用 list中的元素 循环迭代
for i in File:
    print(i+'\n')  #通过print可以看到，这里的i是File里面的一个元素，就是一个文件名
    F= open(D+'\\'+i,'r',encoding='utf-8')    # F是个IO对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    text=F.readline()   #注意readline()只读取F文件中的第1行，读完之后会把光标跳到下一行的开头
    print(text)     #通过循环就能得到所有文件的第一行
    
for i in File:
    F= open(D+'\\'+i,'r',encoding='utf-8')    # F是个对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    text=F.readlines()   #读取F文件中的所有行，读完之后返回一个list，每一行是一个list的元素
    type(text)  #大家要养成多用type()和print()函数的习惯。通过type可以看到text是一个list。学编程两大法宝：type()和print()
    print(text[0])  #通过list切片就能看到第1行的内容
    print(text[1])  #通过list切片就能看到第2行的内容
    print(text[2])  #通过list切片就能看到第3行的内容


# 进阶使用循环嵌套，就是2层循环.读取每一个文件中的所有行。下面几种写法效果都是一样的，只是实现的语法不同    
for i in File: #第一层循环，逐个迭代文件
    F= open(D+'\\'+i,'r',encoding='utf-8')    # F是个对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    text=F.readlines()   #读取F文件中的所有行，读完之后返回一个list，每一行是一个list的元素
    for line in text:  #第二层循环，读取文件中的每一行，readlines()函数会取出F中的所有行，通过迭代，line每次会取出一行
        print(line+'\n')     #通过循环就能得到所有文件的每一行内容 +'\n'在每一行结尾加换行符，让格式更易读。

for i in File: #第一层循环，逐个迭代文件
    F= open(D+'\\'+i,'r',encoding='utf-8')    # F是个IO对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    for line in F.readlines():  #第二层循环，不用text变量，line直接在F.readlines()里面迭代也是可以的。
                                #上面一种写法引入变量text主要是为了方便初学者在变量浏览器中查看text=F.readlines()的内容
        print(line+'\n')     #通过循环就能得到所有文件的第一行

for i in File: #第一层循环，逐个迭代文件
    F= open(D+'\\'+i,'r',encoding='utf-8')    # F是个对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    type(F)     # 这里F的类型是IO库里的_io.TextIOWrapper（文本文件IO容器 ）
    for line in F:  #第二层循环，不使用readlines()函数也行，因为F这个文本文件容器对象本身已经包含了文件的所有内容
        print(line+'\n')     #通过循环就能得到所有文件的第一行


    
#第2种：用 数字 循环迭代
for i in range(0,len(File),1):
    F= open(D+'\\'+File[i],'r',encoding='utf-8')   # F是个对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    for j in range(0,3,1):  # 这里我知道文件只有是3行所以直接写0-3范围,但是很多时候是不知道文件有多少行，所以这种方法并不好用
        text=F.readline()  # 读取对象F中的第1行,读取完后将光标跳到下一行的开头处
        print(text+'\n')

for i in range(0,len(File),1):
    F= open(D+'\\'+File[i],'r',encoding='utf-8')    # F是个对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    text=F.readlines()   #读取F文件中的所有行，读完之后返回一个list，每一行是一个list的元素
    for j in range(0,len(text),1):  #通过len()函数取text得长度，通过变量j依次迭代每一个元素
        print(text[j]+'\n')  # 通过数字的迭代，依次取出第1,2,3 行,每一行后面都加换行符让格式好看

#进阶，将5个文件的内容写入到一个txt文件中保存:    
#首先要创建一个供写入的文件对象
file = open(r'D:\test\file .txt','a',encoding='utf-8')     #新建一个供写入的对象file，对应文件D:\test\file.txt

for i in File: #第一层循环，逐个迭代文件
    F= open(D+'\\'+i,'r',encoding='utf-8')    # F是个对象用来打开文件,'r'是读取 'utf-8'是解码方式，打开中文必须定义
    for line in F:  
        F.write(line+'\n')
    F.write('\n')    #这一句write的作用是每写完一个文件在末尾加个换行，不然两个文件之间是连在一起的，大家可以注释掉这句看看效果
F.close()  #写完之后关闭文件。


def write_to_file(content):       #定义输出到文件的程序
#==============================================================================
#     定义一个输出到文件的函数
#==============================================================================
    with open(r'D:\python\movielist.txt','a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8，'a'表示追加写入
        f.write(content+'\n')      #打开写入文件编码方式：utf-8    



'''
你们应该会得到一个file.txt,里面的内容是：
冯明山 男 38岁

1980-11-30

网络优化
。。。。。。。。。。。。。。。。。。
今天的内容就到这里，学编程关键是多写代码，执行，看变量，看结果，看不明白的多用 两大法宝：type()和print() 
单纯复制粘贴是不行的，看明白了自己敲，敲错了再改错才能掌握语言的语法和格式。

''' 



    







 
