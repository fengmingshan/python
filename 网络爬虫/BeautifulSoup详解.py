# -*- coding: utf-8 -*-
"""
Created on Fri May  1 07:57:25 2020

@author: Administrator
"""

import bs4
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html)

# soup = BeautifulSoup(open('index.html')) #用本地文件来创建soup对象

# 打印一下 soup 对象的内容，格式化输出
print(soup.prettify())

# =============================================================================
# Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:
#     Tag
#     NavigableString
#     BeautifulSoup
#     Comment
# 下面我们进行一一介绍
# =============================================================================

# =============================================================================
# (1) Tag
# =============================================================================

#Tag 是什么？ Tag 是HTML 中的一个个标签例如:
#<title>The Dormouse's story</title>
#<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

# 利用 soup加标签名轻松地获取这些标签的内容,它查找的是在所有内容中的第一个符合要求的标签
print(soup.title)

print(soup.head)

print(soup.a)

print(soup.p)

print(type(soup.a))

# Tag，它有两个重要的属性，是 name 和 attrs
print(soup.name)
print(soup.head.name)

print(soup.p['class'])

print(soup.p.get('class'))

#还可以利用get方法，传入属性的名称
soup.p['class']="newClass"
print(soup.p)

#还可以对这个属性进行删除，例如
del soup.p['class']
print(soup.p)


# (2) NavigableString

#们要想获取标签内部的文字怎么办呢？
print(soup.p.string)

print( type(soup.p.string))

print( type(soup.name))

print(soup.name )

print(soup.attrs)


# (3) BeautifulSoup

# BeautifulSoup 对象表示的是一个文档的全部内容
print( type(soup.name))

print( soup.name )

print( soup.attrs )

# (4) Comment

#Comment 对象是一个特殊类型的 NavigableString 对象

print(soup.a)
# a 标签里的内容实际上是注释，但是如果我们利用 .string 来输出它的内容，
# 我们发现它已经把注释符号去掉了
print(soup.a.string)
print(type(soup.a.string))

# 所以，我们在使用前最好做一下判断，判断代码如下
if type(soup.a.string)==bs4.element.Comment:
    print(soup.a.string)


# =============================================================================
# 遍历文档树
# =============================================================================

# （1）直接子节点

# .contents
# tag 的 .content 属性可以将tag的尖括号中的内容以列表的形式返回
print(soup.head.contents)
print(soup.body.contents)

html1 = """
<head><title>one</title>
<title>two</title>
<title>three</title></head>
"""
soup1 = BeautifulSoup(html1)
print(soup1.head.contents)



# 输出方式为列表，我们可以用列表索引来获取它的某一个元素
print(soup1.head.contents[0])

# .children
#  .children 是一个 list 生成器对象
print(soup1.head.children)

# 遍历就能获得里面的内容
for child in soup1.head.children:
  print(child)

# 遍历就能获得里面的内容
for child in soup.body.children:
  print(child)


# （2）所有子孙节点

# .descendants
# .descendants 属性可以对所有tag的子孙节点进行递归循环，返回一个生成器
for child in soup.descendants:
    print(child)


# （3）节点内容

# .string 属性
# 如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。
# 如果一个标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容。
# 以下两个语句返回的都是title里的text
print(soup.head.string)
print(soup.title.string)

# 如果tag包含了多个子节点,tag就无法确定，string 方法应该调用哪个子节点的内容。
# .string 的输出结果是 None
print(soup.html.string)
print(soup.body.string)


# （4）多个内容

# .strings
# 获取多个内容，不过需要遍历获取，比如下面的例子
for string in soup.strings:
    print(repr(string))

# .stripped_strings
# 输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除空白内容
for string in soup.stripped_strings:
    print(repr(string))


# （5）父节点

print(soup.p.parent.name)

content = soup.head.title.string
content
print(content.parent.name)

print(soup.head.title.parent.name)

print(soup.body.parent.name)


# （6）全部父节点

# 通过元素的 .parents 属性可以递归得到元素的所有父辈节点
content = soup.a.string
content
for parent in content.parents:
    print(parent.name)

for parent in soup.a.parents:
    print(parent.name)


# （7）兄弟节点

# .next_sibling .previous_sibling 属性

# 兄弟节点可以理解为和本节点处在统一级的节点。
# .next_sibling 属性获取了该节点的下一个兄弟节点
# .previous_sibling 则与之相反，
# 如果节点不存在，则返回 None

# 因为两个p标签之间有换行符，空白或者换行也可以被视作一个节点，所以返回了一个换行符
print(repr(soup.p.next_sibling))

# 因为第一个p标签前没有前一个兄弟节点，返回 None
print(soup.p.prev_sibling)

# 因为p标签之间有换行，所以下一个的下一个才是第2个p标签
print(soup.p.next_sibling.next_sibling)

# 因为p标签之间有换行，所以连续四个下一个才是第3个p标签
print(soup.p.next_sibling.next_sibling.next_sibling.next_sibling)


# （9）前后节点

# .next_element .previous_element 属性
# 它并不是针对于兄弟节点，而是在所有节点，不分层次
# 比如 <head><title>The Dormouse's story</title></head>
# 不考虑层次关系，head的下一个节点就是title
print(soup.head.next_element)

# 第一个b标签的上一个元素是p标签
print(soup.b.previous_element)


# 第一个a标签的上一个元素是text
print(soup.a.previous_element)

# 第一个a标签的上两个个元素是p标签
print(soup.a.previous_element.previous_element)


# （10）所有前后节点

# .next_elements .previous_elements 属性
# .next_elements 和 .previous_elements 的迭代器就可以向前或向后访问文档的解析内容
for element in soup.p.next_elements:
    print(repr(element))

for element in soup.a.previous_elements:
    print(repr(element))
