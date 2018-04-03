# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 21:24:31 2018
多进程:multiprocessing
@author: Administrator
"""
from multiprocessing import Process
import os

def run_proc(name):  # 子进程要执行的代码
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')

# 进程Pool
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    

from multiprocessing import Process, Pool
import os
import time

def run_proc(wTime):
    n = 0
    while n < 3:
        print('subProcess %s run' % os.getpid(), "{0}".format(time.ctime()))    #获取当前进程号和正在运行是的时间
        time.sleep(wTime)    #等待（休眠）
        n += 1

if __name__ == "__main__":
    p = Process(target=run_proc, args=(2,))  #申请子进程
    p.start()     #运行进程
    print ('Parent process run. subProcess is', p.pid)
    print ('Parent process end,{0}'.format(time.ctime()))