# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-10-24 19:37:06
# @Last Modified by:   Administrator
# @Last Modified time: 2019-10-24 23:09:26
from wxpy import *
import os

data_path ='D:/Test/wxpy'
os.chdir(data_path)

bot = Bot(console_qr = 2)
bot.messages.max_history = 10000
my_group = bot.groups().search('我们8班')[0]
my_friend = bot.friends().search('刘燕')[0]

@bot.register(my_friend)
def just_print(msg):
    # 打印消息
    print(msg)

bot.file_helper.send('Hello from wxpy!')

# 堵塞线程，并进入 Python 命令行
embed()