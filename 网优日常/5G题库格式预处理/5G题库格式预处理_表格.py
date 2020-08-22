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

select_names  = ['序号','题型','题目','选项A','选项B','选项C','选项D','答案']
judge_names  = ['序号','题型','题目','答案']

df_single = pd.read_excel('./5G应知应会SGS.xlsx',sheet_name = '单选题',header = 1,names =select_names)
df_single['选项'] = 'A: '+ df_single['选项A'].map(str)+ '    '+ \
                    'B: '+ df_single['选项B'].map(str)+ '    '+ \
                    'C: '+ df_single['选项C'].map(str)+ '    '+ \
                    'D: '+ df_single['选项D'].map(str)

df_muti = pd.read_excel('./5G应知应会SGS.xlsx',sheet_name = '多选题',header = 1,names =select_names)
df_muti['选项'] = 'A: '+ df_muti['选项A'].map(str)+ '    '+ \
                    'B: '+ df_muti['选项B'].map(str)+ '    '+ \
                    'C: '+ df_muti['选项C'].map(str)+ '    '+ \
                    'D: '+ df_muti['选项D'].map(str)

df_judge = pd.read_excel('./5G应知应会SGS.xlsx',sheet_name = '判断题',header = 1,names =judge_names)
df_judge['选项'] = '对 or 错'

squence = ['第{}题'.format(str(x)) for x in pd.concat(
    [df_single['序号'],
     df_muti['序号'],
     df_judge['序号'],
     ],axis =0
     )
]

question_type = [x for x in pd.concat(
    [df_single['题型'],
     df_muti['题型'],
     df_judge['题型'],
     ],axis =0
     )
]

question = [x for x in pd.concat(
    [df_single['题目'],
     df_muti['题目'],
     df_judge['题目'],
     ],axis =0
     )
]

options = [x for x in pd.concat(
    [df_single['选项'],
     df_muti['选项'],
     df_judge['选项'],
     ],axis =0
     )
]

answer = [x for x in pd.concat(
    [df_single['答案'],
     df_muti['答案'],
     df_judge['答案'],
     ],axis =0
     )
]

df_questions = pd.DataFrame({
    'no':range(325,325+len(squence)),
    'squence':squence,
    'type':question_type,
    'question':question,
    'options':options,
    'answer':answer,
    'source':'5G应知应会'
    })

with open('5G应知应会.csv','w',newline = '',encoding = 'utf-8') as f:
    df_questions.to_csv(f,index= False)
