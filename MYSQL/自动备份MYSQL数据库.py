# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:06:58 2020

@author: Administrator
"""

import os
import time
import pymysql
import sched # 导入定时任务库
from datetime import datetime
from datetime import timedelta

user = 'root'
pwd = 'a123456'
sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类

def getDatabaseNames():
    conn = pymysql.connect("localhost", user, pwd, use_unicode=True, charset="utf8")
    cur = conn.cursor()
    cur.execute('show databases;')
    dbs = cur.fetchall()
    cur.close()
    conn.close()
    return dbs

# path trim一下然后创建


def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)

    if not isExists:
        os.mkdir(path)
        return True
    else:
        return False


def task():
    sche.enter(86400,1,task)  # 调用sche实例的enter方法创建一个定时任务，86400秒一天之后执行，任务内容执行task()函数
    timestr = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    weekday = datetime.strptime(timestr,"%Y-%m-%d").weekday()+1
    print('周{}，无需备份!'.format(weekday))
    if weekday == 6:
        print('今天是周6，开始执行备份!')
        folder = 'D:/database_bak/'+timestr
        mkdir(folder)

        dbs = getDatabaseNames()
        print(dbs)
        for db in dbs:
            try:
                dbname = db[0]
                # 排除系统自带的db
                if dbname == "mysql" or dbname == "performance_schema" or dbname == "information_schema" or dbname == "sys" or dbname == "syssakilaor" or dbname == "employees" or dbname == "world":
                    continue
                # 导出db
                cmd = "mysqldump -u%s -p%s %s > %s/%s.sql" % (user, pwd, dbname, folder, dbname)
                print(cmd)
                os.system(cmd)
            except Exception as e:
                print(e)
        print('备份完成!')

# =============================================================================
# 延时10秒后启动任务
# =============================================================================
sche.enter(11,1,task)  # 调用sche实力的enter方法创建一个定时任务，11秒之后执行，任务内容执行task()函数

print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)
sche.run()
