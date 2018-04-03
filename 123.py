# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 22:04:06 2018

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
