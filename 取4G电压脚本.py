# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:41:21 2018

@author: Administrator
"""
import pyautogui # 
import sched # 导入定时任务库
import time # 导入time模块

sche=sched.scheduler(time.time,time.sleep)  # 实例化sched.scheduler类

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.5  # 停顿2秒
pyautogui.size()
width, height = pyautogui.size()

def task():
    sche.enter(1800,1,task)  # 调用sche实力的enter方法创建一个定时任务，1800秒之后执行，任务内容执行task()函数
    
    print('任务开始时间:',time.ctime(time.time()))
    
    pyautogui.moveTo(109,246, duration=0.5)   # 找到BSC客户端
    pyautogui.doubleClick()     # 双击打开BSC客户端
    
    pyautogui.moveTo(649,480, duration=0.5)   # 找到密码窗
    pyautogui.click()     # 点击
    
    pyautogui.typewrite('Fms1234567!',0.3)  # 输入密码
    
    
    pyautogui.moveTo(809,557, duration=0.5)   # 找到登录按钮
    pyautogui.click()     # 登录BSC客户端
    
    time.sleep(10)
    
    pyautogui.hotkey('altleft', 'c')
    
    pyautogui.hotkey('altleft', 'e')
    # =============================================================================
    # OMMB1
    # =============================================================================
    pyautogui.moveTo(160,152, duration=0.5)   # 找OMMB1
    pyautogui.click(button='right') 
    pyautogui.moveRel(63,13, duration=0.5)   # 启动网元管理
    pyautogui.click() 
    time.sleep(40)
    
    pyautogui.moveTo(160,152, duration=0.5)   # 找OMMB1
    pyautogui.click(button='right') 
    pyautogui.moveRel(46,129, duration=0.5)   # 找诊断测试
    pyautogui.click() 
    time.sleep(15)
    
    
    
    pyautogui.hotkey('altleft', 'o')
    
    pyautogui.hotkey('altleft', 't')
    
    pyautogui.moveTo(661,242, duration=0.5)   # 找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(34,129, duration=0.5)   # 找到运行
    pyautogui.click() 
    pyautogui.moveTo(689,485, duration=0.5)   # 确定开始运行
    pyautogui.click() 
    
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
    for i in range(0,40,1):                   # 画55次，时间360秒左右
        pyautogui.moveTo(850,300, duration=0.5)   # 画框
        pyautogui.moveTo(850,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,300, duration=0.5)   # 画框
        time.sleep(1)   # 等待任务执行
    
    
    pyautogui.moveTo(661,241, duration=0.5)   # 找到任务找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(44,152, duration=0.5)   # 选择查看任务结果
    pyautogui.click() 
    pyautogui.moveTo(963,175, duration=0.5)   # 找到导出任务结果
    pyautogui.click() 
    pyautogui.moveTo(860,574, duration=0.5)   # 找到保存
    pyautogui.click() 
    time.sleep(15)
    pyautogui.moveTo(680,485, duration=0.5)   # 不转到目录
    pyautogui.click()
    pyautogui.moveTo(682,150, duration=0.5)   # 关闭查询结果
    pyautogui.click()
    
    time.sleep(5)
    
    # =============================================================================
    # OMMB2
    # =============================================================================
    pyautogui.moveTo(155,178, duration=0.5)   # 找OMMB2
    pyautogui.click(button='right') 
    pyautogui.moveRel(63,13, duration=0.5)   # 启动网元管理
    pyautogui.click() 
    time.sleep(40)
    
    pyautogui.moveTo(155,178, duration=0.5)   # 找OMMB2
    pyautogui.click(button='right') 
    pyautogui.moveRel(46,129, duration=0.5)   # 找诊断测试
    pyautogui.click() 
    time.sleep(15)
    
    
    
    pyautogui.hotkey('altleft', 'o')
    
    pyautogui.hotkey('altleft', 't')
        
    pyautogui.moveTo(661,242, duration=0.5)   # 找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(34,129, duration=0.5)   # 找到运行
    pyautogui.click() 
    pyautogui.moveTo(689,485, duration=0.5)   # 确定开始运行
    pyautogui.click() 
    
    
    pyautogui.moveTo(700,300, duration=0.5)   # 移动到中间，画框，等待任务结束
    for i in range(0,20,1):                   # 画55次，时间600秒左右
        pyautogui.moveTo(850,300, duration=0.5)   # 画框
        pyautogui.moveTo(850,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,450, duration=0.5)   # 画框
        pyautogui.moveTo(700,300, duration=0.5)   # 画框
        time.sleep(1)   # 等待任务执行
        
    pyautogui.moveTo(661,241, duration=0.5)   # 找到任务找到任务直流输入电压
    pyautogui.click(button='right') 
    pyautogui.moveRel(44,152, duration=0.5)   # 选择查看任务结果
    pyautogui.click() 
    pyautogui.moveTo(963,175, duration=0.5)   # 找到导出任务结果
    pyautogui.click() 
    pyautogui.moveTo(860,574, duration=0.5)   # 找到保存
    pyautogui.click() 
    time.sleep(15)
    pyautogui.moveTo(680,485, duration=0.5)   # 不转到目录
    pyautogui.click()
    pyautogui.moveTo(682,150, duration=0.5)   # 关闭查询结果
    pyautogui.click()
    time.sleep(5)
    
    pyautogui.hotkey('altleft', 's') # 系统
    
    pyautogui.hotkey('altleft', 'u') # 注销
    
    pyautogui.moveTo(680,487, duration=0.5)   # 确认注销
    pyautogui.click()
    time.sleep(10) 
    pyautogui.moveTo(891,320, duration=0.5)   # 关闭登陆窗
    pyautogui.click()
    pyautogui.moveTo(684,484, duration=0.5)   # 确认退出
    pyautogui.click()
    
    print('任务结束时间:',time.ctime(time.time()))

sche.enter(12,1,task)  # 调用sche实力的enter方法创建一个定时任务，12秒之后执行，任务内容执行task()函数

print('task will run in 10 second') # 提示信息 10秒计时
for i in range(1,11,1):
    print('----->',i)
    time.sleep(1)

sche.run()
   
    
    
    
    
    
    
    
