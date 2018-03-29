# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:41:21 2018

@author: Administrator
"""
import pyautogui
import sched # 导入定时任务库
import time # 导入time模块

sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类
pyautogui.FAILSAFE = False
def task():
    print('任务开始时间:',time.ctime(time.time()))
    sche.enter(1800,1,task)  # 调用sche实力的enter方法创建一个定时任务，400秒之后执行，任务内容执行task()函数
    pyautogui.PAUSE = 1.5   # 停顿2秒
    pyautogui.size()
    width, height = pyautogui.size()
    
    pyautogui.hotkey('winleft', 'd')
    time.sleep(2)
    
    pyautogui.moveTo(108, 215, duration=0.5)   # 找到BSC客户端
    
    pyautogui.doubleClick()     # 双击打开BSC客户端
    
    pyautogui.moveTo(712, 480, duration=0.5)   # 找到密码窗
    pyautogui.click()     # 点击

    
    pyautogui.typewrite('Fms123456!',0.2)  # 输入密码
    
    pyautogui.moveTo(800, 565, duration=0.5)   # 找到登录按钮
    
    pyautogui.click()     # 登录BSC客户端
    
    pyautogui.moveTo(100, 200, 10,pyautogui.easeInOutQuad)   # 延时移动到任意点-徘徊前进，等待登录成功
    
    pyautogui.hotkey('altleft', 'v')
    
    pyautogui.hotkey('altleft', 'f')
    
    pyautogui.hotkey('altleft', 'a')
    
    pyautogui.moveTo(29, 132, duration=0.25)   # 找到基站树
    pyautogui.click()     # 点击
    pyautogui.moveTo(50, 152, duration=0.25)   # 展开基站树
    pyautogui.click()      # 点击
    pyautogui.moveTo(173, 197, duration=0.25)   # 找到任意基站
    pyautogui.click()      # 点击
    
    pyautogui.hotkey('altleft', 'p')
    
    pyautogui.hotkey('altleft', 'f')
    
    pyautogui.moveTo(451, 109, duration=0.25)   # 找到自动保存电压按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(1429,83,duration=180)   # 找到关闭电压窗口按钮-徘徊前进
    pyautogui.click()     # 点击
        
    pyautogui.moveTo(1397, 32, duration=1)  # 找到注销客户端按钮
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(678,484,duration=1)   # 找到确认注销按钮-开始快减速运动
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(892,315,1,pyautogui.easeOutQuad)   # 找到登录窗口关闭按钮-开始快减速运动
    pyautogui.click()     # 点击
    
    pyautogui.moveTo(684,488,1,pyautogui.easeOutQuad)   # 找到登录窗口关闭按钮-开始快减速运动
    pyautogui.click()     # 点击
   
    print('任务结束:',time.ctime(time.time()))
    print('--------------------------------------------------')
       
sche.enter(12,1,task)  # 调用sche实力的enter方法创建一个定时任务，10秒之后执行，任务内容执行task()函数
print('task run in 10 second:')
for i in range(1,11,1):
    print('------>',i)
    time.sleep(1)
sche.run()
