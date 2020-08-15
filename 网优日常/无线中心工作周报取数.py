# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:39:39 2020

@author: Administrator
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path = r'D:\2020年工作\_工作周报'
os.chdir(path)

week = 33

engine_work = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/work_report?charset=utf8",
                            pool_recycle=7200)
Session_work = sessionmaker(autocommit=False, autoflush=True, bind=engine_work)
session_work = Session_work()

work_report = session_work.execute(
    '''(SELECT * from `工作周报`
        WHERE `周` = {week}
        AND `当前状态` != '待反馈'
        AND `姓名` in ('冯明山','王鑫','周朝城','田中玉')
        AND `工作类别` != '安排的工作'
        AND `工作类别` != '学习提升'
        ORDER BY `姓名`,`开始日期` limit 1000)
        UNION
        (SELECT * from `工作周报`
        WHERE `周` = {week}
        AND `当前状态` != '待反馈'
        AND `姓名` in ('解艳刚','史艳丽','查天星')
        AND `工作类别` != '安排的工作'
        AND `工作类别` != '学习提升'
        ORDER BY `姓名`,`开始日期` limit 1000)'''.format(week = week)
)

wireless_report = session_work.execute(
    '''SELECT * from `工作周报` WHERE `周` = {week}
        AND `当前状态` != '待反馈'
        AND `工作类别` != '学习提升'
        AND `姓名` in ('冯明山','王鑫','周朝城','田中玉')
        ORDER BY `姓名`,`开始日期`'''.format(week = week)
)

maintain_report = session_work.execute(
    '''SELECT * from `工作周报`
        WHERE `周` = {week}
        AND `当前状态` != '待反馈'
        AND `工作类别` != '学习提升'
        AND `姓名` in ('解艳刚','史艳丽','查天星')
        ORDER BY `姓名`,`开始日期`'''.format(week = week)
)

work_report = list(work_report)
work_cotent = [x.工作内容 for x in work_report]

wireless_report = list(wireless_report)
wireless_cotent = [x.工作内容 for x in wireless_report]

maintain_report = list(maintain_report)
maintain_cotent = [x.工作内容 for x in maintain_report]

with open('第{week}周工作周报.txt'.format(week = week),'w') as f:
    f.writelines('无线中心全部工作汇总')
    f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
    for num,line in enumerate(work_cotent):
        f.writelines(str(num+1))
        f.writelines('.')
        f.writelines(line)
        f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
        f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
    f.writelines('一、无线网维护方面：')
    f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
    for num,line in enumerate(maintain_cotent):
        f.writelines(str(num+1))
        f.writelines('.')
        f.writelines(line)
        f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
        f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
    f.writelines('二、无线网优化方面：')
    f.writelines('\n')

with open('第{week}周工作周报.txt'.format(week = week),'a') as f:
    for num,line in enumerate(wireless_cotent):
        f.writelines(str(num+1))
        f.writelines('.')
        f.writelines(line)
        f.writelines('\n')

