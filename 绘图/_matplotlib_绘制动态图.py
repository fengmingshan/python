# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:52:08 2019

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
# 动画需要导入该模块
from matplotlib import animation
# 定义动画的速度，通过改变这个变量的值改变动画速度
speed = 0.03

fig, ax = plt.subplots()
x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))

# 每次执行时的函数，


def animate(i):
    line.set_ydata(np.sin(x + i * speed))
    return line,

# 动画初始的方法


def init():
    line.set_ydata(np.sin(x))
    return line,


# fig : 执行动画的图像
# func : 动画的执行函数
# frames : 表示多少次动画为一个循环
# init_func : 动画的初始位置
# interval : 动画执行的间隔  不能为小数,小数动画就不执行了,不知道是不是我的姿势不对
# blit : Mac设置为False,设置为True会报错,根据错误提示如下，可以使用'TKAgg'代替
# matplotlib.animation.BackendError: The current backend is 'MacOSX'and may go into an infinite loop with blit turned on.  Either turn off blit or use an alternate backend, for example, like 'TKAgg', using the following prepended to your source code:
ani = animation.FuncAnimation(fig=fig, func=animate, frames=int(
    2*np.pi/speed), init_func=init, interval=1, blit=False)
# 查看帮助文档
help(ani.save)
# 可以将动画以mp4格式保存下来，但首先要保证你已经安装了ffmpeg 或者mencoder
ani.save('basic_animation.html', fps=30, extra_args=['-vcodec', 'libx264'])
