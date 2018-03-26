# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 22:34:59 2018
test.py
@author: Administrator
"""
import sched # 导入定时任务库
import time # 导入time模块
from datetime import datetime
import subprocess


sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类
n = 0

def task():
    global n
    n = n + 1
    if n < 4:
        sche.enter(10,1,task)  # 调用sche实力的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
        current_time = str(datetime.now()).split('.')[0]
        print('任务开始时间:',current_time)
        for i in range(0,5,1):
            print('----->',i+1)
            time.sleep(1)

        current_time = str(datetime.now()).split('.')[0]
        print('任务结束时间:',current_time)
        print('-------------------')
    else: 
        pass




sche.enter(3,1,task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行task()函数

print('task will run in 3 second') # 提示信息 10秒计时
for i in range(0,3,1):
    print('----->',i+1)
    time.sleep(1)
sche.run()

 

