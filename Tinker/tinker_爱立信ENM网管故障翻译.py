# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 07:19:04 2020

@author: Administrator
"""

from tkinter import Tk,Entry,filedialog,Button,Label,messagebox
from tkinter import StringVar
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import pandas as pd

window = Tk()
window.title("爱立信历史告警翻译")
window.geometry("700x350")

alarm = StringVar()
bts_info = StringVar()
alarm_dict = StringVar()
line_var = StringVar()
global alarm_file,bts_file,alarm_dict,line

def selectalarm():
    global alarm_file
    alarm_file = askopenfilename(filetypes=[("Excel file", "*.csv"),("all","*.*")])
    alarm.set(alarm_file)

def selectbts():
    global bts_file
    bts_file = askopenfilename(filetypes=[("Excel file", "*.xlsx"),("all","*.*")])
    bts_info.set(bts_file)

def selectdict():
    global alarm_dict
    dict_file = askopenfilename(filetypes=[("TxT file", "*.txt"),("all","*.*")])
    alarm_dict.set(dict_file)

def translate():
    global alarm_file,bts_file,alarm_dict,line
    content = pd.read_csv(alarm_file,encoding ='gbk')
    line = content.columns[1]
    line_var.set(content.columns)
    messagebox.showinfo("翻译完成", line)

label1 = Label(window, text="告警文件： ").grid(column=0, row=0)
filename1 = Entry(window, width=40, textvariable = alarm).grid(column=1, row=0)
selete1 = Button(window, text="选择告警文件",command = selectalarm).grid(column=2, row=0)

label2 = Label(window, text="基站信息表： ").grid(column=0, row=1)
filename2 = Entry(window, width=40, textvariable = bts_info).grid(column=1, row=1)
selete2 = Button(window, text="选择基站信息表",command = selectbts).grid(column=2, row=1)

label3 = Label(window, text="告警字典： ").grid(column=0, row=2)
filename3 = Entry(window, width=40, textvariable = alarm_dict).grid(column=1, row=2)
selete3 = Button(window, text="选择告警字典",command = selectdict).grid(column=2, row=2)

translate = Button(window, width=20, text="开始翻译",command = translate).grid(column=4, row=3)
content1 = Entry(window, width=20, textvariable = line_var).grid(column=0, row=3)

window.mainloop()
