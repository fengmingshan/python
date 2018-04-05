# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 21:24:31 2018
多进程:multiprocessing
@author: Administrator
"""
# =============================================================================
# 多进程:multiprocessing
# =============================================================================
from multiprocessing import Process
import os
import time 

def run_proc(name):  # 子进程要执行的代码
    timesleep(random.random() * 10)
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')


from multiprocessing import Process, Pool
import os
import time

def run_proc(wTime):
    n = 0
    while n < 5:
        print('subProcess %s run' % os.getpid(), "{0}".format(time.ctime()))    #获取当前进程号和正在运行是的时间
        time.sleep(wTime)    #等待（休眠）
        n += 1

if __name__ == "__main__":
    p = Process(target=run_proc, args=(2,))  #申请子进程
    p.start()     #运行进程
    print ('Parent process run. subProcess is', p.pid)
    print ('Parent process end,{0}'.format(time.ctime()))

# =============================================================================
# 进程Pool
# =============================================================================
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 10)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):  # 同时创建5个子进程，因为我的电脑是4核的，所以有一个进程需要排队
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()  # 关闭进程池，之后就不能添加新的进程了
    p.join()   # 如果有进程Pool，调用join前必须调用close
    print('All subprocesses done.')
    
    
# 把上面的例子修改一下，模拟5个同学做算术的多进程
# 从这个例子可以更明显的看到进程的执行和排队的过程
from multiprocessing import Pool
import os, time, random

def long_time_task(name,n):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    x = 0
    for i in range(1,n+1,1):            # 给出累加的范围
        x += i                          # 计算累加
        time.sleep(random.random())     # 随机延时
    
    end = time.time()
    print('Task %s runs %0.2f seconds.result = %d' % (name, (end - start),x))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    name_list = ['tom','jerry','kate','lily','lucy']  # 5个同学的名字
    for name in name_list:
        p.apply_async(long_time_task, args=(name,30)) # 启动5个子进程，计算从1到30
    print('Waiting for all subprocesses done...')
    p.close()   # 关闭进程池，之后就不能添加新的进程了
    p.join()    # 如果有进程Pool，调用join前必须调用close
    print('All subprocesses done.')

# =============================================================================
# 进程间通信
# =============================================================================

# Process之间肯定是需要通信的，Python的multiprocessing模块提供了Queue、Pipes等多种方式来交换数据。
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()


# =============================================================================
# 在pool中使用Queue
# =============================================================================

# 在pool中直接使用Queue会报错，因为队列对象不能在父进程与子进程间通信 
# 必须使用multiprocess的Manager类
import multiprocessing
from multiprocessing import Process, Queue
import os, time, random

def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
	manager = multiprocessing.Manager()# 父进程创建Queue，并传给各个子进程：
	q = manager.Queue()
	p = Pool(4)
	pw = p.apply_async(write,args=(q,))
	time.sleep(0.5)
	pr = p.apply_async(read,args=(q,))
	p.close()
	p.join()
	printprint('所有数据都写入并且读完')

# =============================================================================
# 分布式进程
# =============================================================================

# task_master.py
    
__author__ = 'sergiojune'   # 表示代码的作者 
import queue, random
from multiprocessing.managers import BaseManager
# 此文件用来发送和接受结果，test36.py用于处理结果

# 创建通信工具
# 发送任务
post_task = queue.Queue()
# 接受结果
result_task = queue.Queue()


class QueueManager(BaseManager):
    pass

# 定义的函数解决下面的坑
def posttq():
    return post_task

def resulttq():
    return result_task

def start():
    # 注册任务
    # 这里有个坑，在window系统下callable不能为匿名函数，原因是不能被序列化，所以在这里我们需要定义函数
    QueueManager.register('post_task_queue', callable=posttq)  # 第一个参数为注册名字
    QueueManager.register('result_task_queue', callable=resulttq)

    # 绑定窗口，设置验证码
    manager = QueueManager(address=('127.0.0.1', 500), authkey=b'abc')  # 第一个参数为地址和端口，第二个参数为验证码，防止别人骚扰

    # 启动管理
    manager.start()
    # 通过管理器获取通信
    post = manager.post_task_queue()
    result = manager.result_task_queue()

    # 进行发送数据
    print('try post data')
    for x in range(10):
        n = random.randint(1, 1000000)
        print('put %d' % n)
        post.put(n)

    # 接受结果
    print('try get result')
    for x in range(10):
        # timeout表示超时获取数的最长时间
        value = result.get(timeout=10)
        print('get result', value)

    # 关闭管理器
    manager.shutdown()
    print('master end')

if __name__ == '__main__':
    start()



# task_worker.py

__author__ = 'sergiojune'   # 表示代码的作者 
from multiprocessing.managers import BaseManager
import time, queue

class QueueManager(BaseManager):
    pass

# 注册到网络上
QueueManager.register('post_task_queue')  # 由于只是从网络上获取queue，所以不需要写callable方法
QueueManager.register('result_task_queue')
# 连接到网络
address = '127.0.0.1'  # 这个是网络地址
manager = QueueManager(address=(address, 500), authkey=b'abc')  # 这些必须与发送的一致，要不会连不上
# 连接
manager.connect()
# 获取queue
post = manager.post_task_queue()
result = manager.result_task_queue()

# 处理数据
print('tyr get value')
for x in range(10):
    try:
        v = post.get(timeout=10)
        print('get value %d' % v)
        r = v*v
        print('put value %d to result' % r)
        time.sleep(1)
        result.put(r)
    except queue.Empty as e:
        print('Queue is empty')
print('work exit')