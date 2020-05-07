import jieba
import re

symbol_map = {
    ord('\n'): None,
    ord('\t'): None,
    ord('\r'): None,
    ord('①'): None,
    ord('②'): None,
    ord('③'): None,
    ord('④'): None,
    ord('【'): None,
    ord('】'): None,
    ord('('): None,
    ord(')'): None,
    ord('（'): None,
    ord('）'): None,
    ord('：'): None,
    ord(':'): None,
    ord('-'): None,
    ord('；'): None,
    ord(';'): None,
    ord('，'): None,
    ord(','): None,
    ord('。'): None,
    ord('.'): None,
    ord('、'): None,
    ord('-'): None,
    ord('—'): None,
    ord('/'): None,
}


#定义读取停词表的函数
def loadStopWords():
    stop = []
    for line in open('./stopWord.txt').readlines():
        stop.append(line)
    return list(set(stop))


def replace_spcial(msg):
    msg = msg.replace('<br>','')
    msg = msg.replace('<b>','')
    msg = msg.replace('</b>','')
    msg = msg.replace('->','')
    msg = msg.replace('>', '')
    return msg


#定义切词函数
def cutWords(msg,stopWords):
    jieba.load_userdict("./userdict.txt")
    arr_leftWords=[]
    seg_list = jieba.cut(msg,cut_all=False)
    leftWords=''
    for i in seg_list:#for i in y,y可以是列表、元组、字典、Series
        if (i not in stopWords):
            leftWords+=' '+i
    leftWords.strip()
    arr_leftWords.append(leftWords)
    return arr_leftWords