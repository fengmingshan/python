# -*- coding: utf-8 -*-
"""
Created on Sat May  2 08:56:01 2020

@author: Administrator
"""

import bs4
from bs4 import BeautifulSoup


html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
<p class="story" data-foo = "value">foo</p>
"""
soup = BeautifulSoup(html)


# =============================================================================
#（1）find_all( name , attrs , recursive , text , **kwargs )
# find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
# =============================================================================

# =============================================================================
#  1）name 参数
# =============================================================================
# name 参数可以查找所有名字为 name 的tag

# A.传字符串
# 在搜索方法中传入一个字符串参数,Beautiful Soup会查找与字符串完整匹配的内容,

# 下面的例子用于查找文档中所有的<b>标签和<a>标签
soup.find_all('b')

soup.find_all('a')

# B.传正则表达式
# 如果传入正则表达式作为参数,Beautiful Soup会通过正则表达式的 match() 来匹配内容.

# 下面例子中找出所有以b开头的标签,这表示<body>和<b>标签都应该被找到
import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

# C.传列表
# 如果传入列表参数,Beautiful Soup会将与列表中任一元素匹配的内容返回.

# 下面代码找到文档中所有<a>标签和<b>标签
soup.find_all(["a", "b"])

# D.传 True
# True 可以匹配任何值,下面代码查找到所有的tag,但是不包含字符串节点
soup.find_all(True)


# E.传方法
# 如果没有合适过滤器,那么还可以定义一个方法,方法只接受一个元素参数

# 下面方法校验了当前元素,如果包含 class 属性且不包含 id 属性,返回 True:
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
soup.find_all(has_class_but_no_id)

def has_class_and_id(tag):
    return tag.has_attr('class') and  tag.has_attr('id')
soup.find_all(has_class_and_id)

def has_href(tag):
    return tag.has_attr('href')
soup.find_all(has_href)

# =============================================================================
# 2）keyword 参数
# =============================================================================

soup.find_all(id='link2')

soup.find_all(href=re.compile("elsie"))

# 多个参数可以同时过滤tag的多个属性
soup.find_all(href=re.compile("elsie"), id='link1')

soup.find_all(href=re.compile("elsie"), id='link2')

# 我们想用 class 过滤，但class 是 python保留关键字， 加个下划线就可以
soup.find_all("a", class_="sister")

# 有些tag属性在搜索不能使用,比如HTML5中的 data-* 属性
# 下面的语句会报错，因为关键字不能带'-'符号
soup.find_all(data-foo="value")

# 但是可以通过 find_all() 方法的 attrs 参数定义一个字典参数来搜索包含特殊属性的tag
soup.find_all(attrs={"data-foo": "value"})

# =============================================================================
# 3）text 参数
# =============================================================================
# 通过 text 参数可以搜搜文档中的字符串内容.与 name 参数的可选值一样,
# text 参数接受 字符串 , 正则表达式 , 列表, True
soup.find_all(text="Elsie")


soup.find_all(text=["Tillie", "Elsie", "Lacie"])

soup.find_all(text=re.compile("Dormouse"))

# =============================================================================
# 4）limit 参数
# =============================================================================
# find_all() 方法返回全部的搜索结构,如果文档树很大那么搜索会很慢.
# 如果不需要全部结果,可以使用 limit 参数限制返回结果的数量.效果与SQL中的limit关键字类似,
soup.find_all("a", limit=2)

# =============================================================================
# 5）recursive 参数
# =============================================================================
# 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点.
# 如果只想搜索tag的直接子节点,可以使用参数 recursive=False

soup.html.find_all("title")

soup.html.find_all("title", recursive=False)


# =============================================================================
# （2）find( name , attrs , recursive , text , **kwargs )
# =============================================================================
# 它与 find_all() 方法唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表
# 而 find() 方法直接返回结果
soup.html.find("a")
soup.html.find("p",class_= "story")


# =============================================================================
# （3）find_parents() find_parent()
# =============================================================================

#find_all() 和 find() 只搜索当前节点的所有子节点,孙子节点等。
#find_parents() 和 find_parent() 用来搜索当前节点的父辈节点,搜索方法与普通tag相同。


# =============================================================================
# （4）find_next_siblings() find_next_sibling()
# =============================================================================

#.next_siblings 属性对当 tag 的所有后面解析的兄弟 tag 节点进行迭代,
#.find_next_siblings() 方法返回所有符合条件的后面的兄弟节点,
#.find_next_sibling() 只返回符合条件的后面的第一个tag节点


# =============================================================================
# （5）find_previous_siblings() find_previous_sibling()
# =============================================================================

#.previous_siblings 属性对当前 tag 的前面解析的兄弟 tag 节点进行迭代,
#.find_previous_siblings() 方法返回所有符合条件的前面的兄弟节点,
#.find_previous_sibling() 方法返回第一个符合条件的前面的兄弟节点


# =============================================================================
# （6）find_all_next() find_next()
# =============================================================================

#.next_elements 属性对当前 tag 的之后的 tag 和字符串进行迭代,
#.find_all_next() 方法返回所有符合条件的节点,
#.find_next() 方法返回第一个符合条件的节点


# =============================================================================
# 7）find_all_previous() 和 find_previous()
# =============================================================================

#.previous_elements 属性对当前节点前面的 tag 和字符串进行迭代,
#.find_all_previous() 方法返回所有符合条件的节点,
#.find_previous()方法返回第一个符合条件的节点

# （2）（3）（4）（5）（6）（7）方法参数用法与 find_all() 完全相同，