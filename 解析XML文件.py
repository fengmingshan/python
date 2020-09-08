# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 16:32:43 2020

通过minidom解析xml文件

@author: Administrator
"""



import xml.dom.minidom as xmldom
import os


path = r'D:\_python小程序\解析XML文件'
os.chdir(path)


'''
XML文件读取
<?xml version="1.0" encoding="utf-8"?>
<catalog>
    <maxid>4</maxid>
    <login username="pytest" passwd='123456'>dasdas
        <caption>Python</caption>
        <item id="4">
            <caption>测试</caption>
        </item>
    </login>
    <item id="2">
        <caption>Zope</caption>
    </item>
</catalog>

'''

xmlfilepath = "./test.xml"

# 得到文档对象
domobj = xmldom.parse(xmlfilepath)
print("xmldom.parse:", type(domobj))
# 得到元素对象
elementobj = domobj.documentElement
print ("domobj.documentElement:", type(elementobj))

#获得子标签
subElementObj = elementobj.getElementsByTagName("login")
print ("getElementsByTagName:", type(subElementObj))

print (len(subElementObj))
# 获得标签属性值
print (subElementObj[0].getAttribute("username"))
print (subElementObj[0].getAttribute("passwd"))

#区分相同标签名的标签
subElementObj1 = elementobj.getElementsByTagName("caption")
for i in range(len(subElementObj1)):
    print ("subElementObj1[i]:", type(subElementObj1[i]))
    print (subElementObj1[i].firstChild.data)  #显示标签对之间的数据