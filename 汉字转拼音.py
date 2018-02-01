# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:07:22 2018

@author: Administrator
"""
#hanzi2pinyin函数
#原来的hanzi2pinyin函数:
def hanzi2pinyin(self, string=""):
    result = []
    if not isinstance(string, unicode):
        string = string.decode("utf-8")
        
    for char in string:
        key = '%X' % ord(char)
        result.append(self.word_dict.get(key, char).split()[0][:-1].lower())
    return result

#修改后的hanzi2pinyin函数:
def hanzi2pinyin(self, string=""):
    result = []
    if not isinstance(string, unicode):
        string = string.decode("utf-8")

    for char in string:
        key = '%X' % ord(char)
        if not self.word_dict.get(key):
            result.append(char)
        else:
            result.append(self.word_dict.get(key, char).split()[0][:-1].lower())
    return result


#hanzi2pinyin_split函数
#原来的hanzi2pinyin_split函数:
def hanzi2pinyin_split(self, string="", split=""):
    result = self.hanzi2pinyin(string=string)
    if split == "":
        return result
    else:
        return split.join(result)
    
#修改后的hanzi2pinyin_split函数(不论split参数是否为空,hanzi2pinyin_split均返回字符串):    
def hanzi2pinyin_split(self, string="", split=""):
    result = self.hanzi2pinyin(string=string)
    #if split == "":
    #    return result
    #else:
    return split.join(result)