# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 15:27:02 2018

@author: Administrator
"""

import pyautogui
import time
import sched

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.5     # 每条命令之间的间隔设置为2s

sche = sched.scheduler(time.time, time.sleep)   #实例化 sched.scheduler类，有两个参数，当前时间和等待时间。

def task():
    sche.enter(30,1, task)  # 调用sche实例的enter方法创建任务，延时5秒，优先级1，任务内容：执行函数task()
    print ("任务开始时间:",time.ctime(time.time()))
    screenWidth, screenHeight = pyautogui.size()
    
    #x, y = pyautogui.position()    # 获得鼠标当前位置
    pyautogui.moveTo(345,20)
    
    pyautogui.doubleClick()
    
    pyautogui.hotkey('altleft',  'm')
    
    pyautogui.hotkey('ctrl',  'f')
    
    pyautogui.typewrite('python', interval=0.1)
    
    pyautogui.press('enter')
    
    pyautogui.hotkey('altleft', 's')
    
    pyautogui.moveTo(922,251,duration=1)    # 在2秒内移动到坐标，时间越长移动越慢 
    
    pyautogui.click()
    
    pyautogui.moveTo(1344,10,duration=1)
    
    pyautogui.click()
    
    print ("任务结束时间:",time.ctime(time.time()))
    print ('----------------------------------------')

    
sche.enter(6,1, task)  # 调用sche实例的enter方法创建任务，延时5秒，优先级1，任务内容：执行函数task()
sche.run() # 执行上面所有的定义好的延时任务。
print('task start in 5 seconds)
for i in range(0,5,1):
    print(i)
    time.sleep(1)




