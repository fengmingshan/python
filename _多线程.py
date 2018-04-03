# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:02:42 2018

@author: Administrator
"""

import time
import threading

# 新线程执行的代码:
def loop():     #定义传入子线程的函数
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)
# =============================================================================
# 由于任何进程默认就会启动一个线程，我们把该线程称为主线程，主线程又可以启动新的线程，
# Python的threading模块有个current_thread()函数，它永远返回当前线程的实例。
# 主线程实例的名字叫MainThread，子线程的名字在创建时指定，我们用LoopThread命名子线程。
# 名字仅仅在打印时用来显示，完全没有其他意义，如果不起名字Python就自动给线程命名为Thread-1，Thread-2……
# =============================================================================

# =============================================================================
# 多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响。
# 而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，
# 因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。
# 来看看多个线程同时操作一个变量怎么把内容给改乱了：
# =============================================================================
balance = 0     # 假定这是你的银行存款:
def change_it(n):  # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

# =============================================================================
# 如果我们要确保balance计算正确，就要给change_it()上一把锁，当某个线程开始执行change_it()时，
# 我们说，该线程因为获得了锁，因此其他线程不能同时执行change_it()，只能等待，
# 直到锁被释放后，获得该锁以后才能改。由于锁只有一个，无论多少线程，
# 同一时刻最多只有一个线程持有该锁，所以，不会造成修改的冲突。
# 创建一个锁就是通过threading.Lock()来实现：
# =============================================================================
balance = 0
lock = threading.Lock()
def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()

# =============================================================================
# ThreadLocal :全局对象，同时能给每个线程设定不同的属性，避免每个线程都要查字典获取自己的属性名
# =============================================================================
import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()    # 实力化全局对象 threading.local()
def process_student():
    # 获取当前线程关联的student:
    std = local_school.student      # 对学生姓名std赋值
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name     # 对全局对象赋值
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
# =============================================================================
# 全局变量 local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，
# 但互不影响。你可以把local_school看成全局变量，但每个属性如local_school.student都是线程的局部变量，
# 可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。
# =============================================================================

