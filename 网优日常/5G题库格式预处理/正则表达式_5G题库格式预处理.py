# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 09:42:46 2020

@author: Administrator
"""


import re
import pandas as pd
import os

path = r'D:\_python小程序\5G题库格式预处理'
os.chdir(path)

with open('./5G中级题库汇总版_修正格式.txt','r',encoding = 'utf-8') as f:
    text = f.read()
    p = r'(第.+?题.*[\s\S]+?[答案|答]：.*)'
    pattern = re.compile(p)
    questions = pattern.findall(text)

    p_squence = r'(第.+?题.*)'
    pattern_squence  = re.compile(p_squence)
    squence = [re.search(pattern_squence,x).group(0) for x in questions]

    p_question = r'(问题.*[\s\S]+?)A\.'
    pattern_squence  = re.compile(p_question)
    question = [re.search(pattern_squence,x).group(1) for x in questions]
    question = [x.strip().replace('\n','') for x in question]
    question = [x.replace(' ','') for x in question]

    p_options = r'(A\..*[\s\S]+?)答案'
    pattern_options  = re.compile(p_options)
    options =[re.search(pattern_options,x).group(1) for x in questions]
    options =[x.strip().replace('\n','\t') for x in options]

    p_answer = r'(答案.*)'
    pattern_answer  = re.compile(p_answer)
    answer =[re.search(pattern_answer,x).group(0) for x in questions]
    answer =[x.strip().replace('\n','') for x in answer]

    question_type = ['多选题' if len(x.split('：')[1].strip())>1  else '单选题' for x in answer]

df_questions = pd.DataFrame({
    'no':range(1,len(questions)+1),
    'squence':squence,
    'type':question_type,
    'question':question,
    'options':options,
    'answer':answer,
    'source':'5G中级题库汇总版'
    })

with open('5G中级题库汇总版.csv','w',newline = '',encoding = 'utf-8') as f:
    df_questions.to_csv(f,index= False)
