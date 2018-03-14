# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 00:10:52 2018

@author: Administrator
"""

import pyautogui
# 屏幕分辨率，坐标
pyautogui.size() # 显示屏幕分辨率

screenWidth, screenHeight = pyautogui.size() # 获取屏幕分辨率

currentMouseX, currentMouseY = pyautogui.position() # 获取鼠标当前坐标 

x, y = pyautogui.position() # 获得鼠标所在坐标
print(x,y)

# 实时获得鼠标坐标
try:
    while True:
        x, y = pyautogui.position()
        print(x,y)
except KeyboardInterrupt:
    print('\nExit.')

# 鼠标移动_点击
pyautogui.moveTo(100, 150)      # 移动到绝对坐标

pyautogui.click()   # 鼠标单击

pyautogui.doubleClick()  # 鼠标双击

pyautogui.moveRel(None, 10) # 鼠标下移10个像素
#下面是一些带特效的运动方式

pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad) #  开始很慢，不断加速

pyautogui.moveTo(100, 100, 2, pyautogui.easeOutQuad) #  开始很快，不断减速

pyautogui.moveTo(100, 100, 2, pyautogui.easeInOutQuad) #  开始和结束都快，中间比较慢

pyautogui.moveTo(100, 100, 2, pyautogui.easeInBounce) #  一步一徘徊前进

pyautogui.moveTo(100, 100, 2, pyautogui.easeInElastic) #  徘徊幅度更大，甚至超过起点和终点

# 键盘输入
pyautogui.typewrite('Hello world!', interval=0.2) # 键盘输入Hello world!每个字符停顿0.2s

# 按键与热键
pyautogui.press('esc') # 按下esc键
pyautogui.keyDown('shift') # 按下shift键
pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left']) # 连续按6次左键
pyautogui.keyUp('shift') # 松开shift键
pyautogui.hotkey('ctrl', 'c') # 按下热键ctrl+c

# 中断
pyautogui.FAILSAFE = True  #设置后False可关闭中断
pyautogui.PAUSE = 2 # 每条指令间隔2s，全局参数。设置后针对全局生效，不设置默认0.1s，所有的PyAutoGUI函数在延迟完成前都处于阻塞状态（block）

# 鼠标点击
pyautogui.click(x=cur_x, y=cur_y, button='left') #鼠标点击，默认点击当前坐标

pyautogui.doubleClick() # 鼠标双击，其实就是执行两次click()函数

pyautogui.rightClick() # 右击

pyautogui.middleClick() # 中击

pyautogui.click(clicks=2) # 双击左键

pyautogui.click(clicks=2, interval=0.25) # 双击左键，两次间隔0.25s

pyautogui.click(button='right', clicks=2, interval=0.25) # 双击右键，两次间隔0.25s

#滚屏
pyautogui.scroll(200) # 滚屏200像素，只能是正整数

#截屏
pyautogui.screenshot('foo.png') # 截取屏幕

im = pyautogui.screenshot(region=(0, 0, 300 ,400)) # 截取区域，开始坐标，结束坐标

# 按键
pyautogui.keyDown(key_name) # 按下键
pyautogui.keyUp(key_name) # 松开键
pyautogui.keyDown('altleft')  # 按热键 alt+f4
pyautogui.press('f4');
pyautogui.keyUp('altleft') 

pyautogui.hotkey('altleft', 'f4') # 按热键 alt+f4

# 消息弹窗函数，需要用户点确认或者cancel 
pyautogui.alert('这个消息弹窗是文字+OK按钮') 
pyautogui.confirm('这个消息弹窗是文字+OK+Cancel按钮')
pyautogui.prompt('这个消息弹窗是让用户输入字符串，单击OK')

#举个栗子:鼠标画圆
import math
width, height = pyautogui.size()
 
r = 250  # 圆的半径

o_x = width/2  # 圆心x坐标
o_y = height/2  # 圆心y坐标
 
pi = 3.1415926
 
for i in range(2):   # 转10圈
    for angle in range(0, 360, 5):  # 利用圆的参数方程
        X = o_x + r * math.sin(angle*pi/180)
        Y = o_y + r * math.cos(angle*pi/180)
        pyautogui.moveTo(X, Y, duration=0.1)

'''
PyAutoGUI键盘表：
‘enter’(或‘return’ 或 ‘\n’),回车
‘esc’,ESC键
‘shiftleft’, ‘shiftright’,左右SHIFT键
‘altleft’, ‘altright’,左右ALT键
‘ctrlleft’, ‘ctrlright’,左右CTRL键
‘tab’ (‘\t’),TAB键
‘backspace’, ‘delete’,BACKSPACE 、DELETE键
‘pageup’, ‘pagedown’,PAGE UP 和 PAGE DOWN键
‘home’, ‘end’,HOME 和 END键
‘up’, ‘down’, ‘left’,‘right’,箭头键
‘f1’, ‘f2’, ‘f3’….,F1…….F12键
‘volumemute’, ‘volumedown’,‘volumeup’
‘pause’,PAUSE键
‘capslock’, ‘numlock’,‘scrolllock’,CAPS LOCK, NUM LOCK, 和 SCROLLLOCK 键
‘insert’,INS或INSERT键
‘printscreen’,PRTSC 或 PRINT SCREEN键
‘winleft’, ‘winright’,Win键
'''


