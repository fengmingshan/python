# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:09:37 2018
获取鼠标当前坐标
@author: Administrator
"""

import pyautogui
import pyperclip
screenWidth, screenHeight = pyautogui.size() # 获取屏幕分辨率
x, y = pyautogui.position() # 获得鼠标所在坐标
print('( ' + str(x) + ' , ' + str(y) + ' )')
pyperclip.copy('pyautogui.moveTo({},{},duration=0.3)\n pyautogui.doubleClick()'.format(x,y))