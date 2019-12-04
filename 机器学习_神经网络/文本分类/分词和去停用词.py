import jieba
import time
import string
import jieba.analyse


line = '用户因在云南省昆明市呈贡县呈贡大学城雨花毓秀商铺内4G有信号网速慢。引发用户投诉。到用户投诉地点现场测试正常，用户反映问题非无线网络问题，建议用户到附近营业厅检查卡或终端问题。'

# =============================================================================
# 分词
# =============================================================================
#创建分词函数
def cut_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    outstr = ''
    for word in sentence_seged:
        outstr += word
        outstr +=' '
    return outstr


line_seg = cut_sentence(line)


# =============================================================================
# 去停用词
# =============================================================================
stop_word_path = 'D:/Notebook/通过机器学习进行投诉分类/stopWord.txt'

#创建读取停用词函数
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath,'r').readlines()]
    return stopwords

stopwords = stopwordslist(stop_word_path)

#创建去停用词函数
def drop_stop_words(line_seged,stopwords):
    word_list = line_seged.split(' ')
    outstr = ''
    for word in word_list:
        if word not in stopwords:
            outstr += word
            outstr +=' '
    return outstr

drop_stop_words =  drop_stop_words(line_seged,stopwords)

word_list = line_seged.split(' ')
outstr = ''
for word in word_list:
    if word not in stopwords:
        outstr += word
        outstr +=' '
