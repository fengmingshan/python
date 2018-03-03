# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 08:35:22 2018

@author: Administrator
"""

# Base64编解码测试：
str1 = 'This is Test String'
str1=str1.encode('utf-8')
enTest = base64.encodestring(str1)
print('编码后：',enTest)
#对字符串进行解码
deTest = base64.decodestring(enTest)
print('解码后：',deTest)

# python3不太一样：因为3.x中字符都为unicode编码，而b64encode函数的参数为byte类型，所以必须先转码。
import base64 encodestr = base64.b64encode('abcr34r344r'.encode('utf-8')) print(encodestr)

'''
打印结果为
b'YWJjcjM0cjM0NHI='
结果和我们预想的有点区别，我们只想要获得YWJjcjM0cjM0NHI=，而字符串被b''包围了。
这时肯定有人说了，用正则取出来就好了。。。别急。。。
b 表示 byte的意思，我们只要再将byte转换回去就好了。。。源码如下
'''
str = base64.b64encode('abcr34r344r'.encode('utf-8')) 
print(str(encodestr,'utf-8'))

打印结果为
YWJjcjM0cjM0NHI=

# base64编解码
import base64
copyright = 'Copyright (c) 2012 Doucube Inc. All rights reserved.'

def main():
    #转成bytes string
    bytesString = copyright.encode(encoding="utf-8")
    print(bytesString)

    #base64 编码
    encodestr = base64.b64encode(bytesString)
    print(encodestr)
    print(encodestr.decode())

    #解码
    decodestr = base64.b64decode(encodestr)
    print(decodestr.decode())

if __name__ == '__main__':
    main()

