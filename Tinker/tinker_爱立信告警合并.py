# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:32:52 2020

@author: Administrator
"""
from tkinter import Tk,Entry,filedialog,Button,Label,messagebox
from tkinter import StringVar
from tkinter.filedialog import askopenfilenames
from tkinter.scrolledtext import ScrolledText
import pandas as pd

window = Tk()
window.title("爱立信历史告警翻译")
window.geometry("700x350")

files = StringVar()
bts_info = StringVar()
alarm_dict = StringVar()
line_var = StringVar()
global alarm_file,bts_file,alarm_dict,line

def selectalarm():
    global alarm_file
    alarm_file = askopenfilenames(filetypes=[("Excel file", "*.csv"),("all","*.*")])
    files.set(alarm_file)


def get_file_path(self,fname):
    file_path = ''
    if isinstance(fname,list):
        path_list = fname[0].split('/')
    else:
        path_list = fname.split('/')
    del(path_list[-1])
    for string in path_list:
        file_path = file_path + string + '\\'
    return file_path

label1 = Label(window, text="告警文件： ").grid(column=0, row=0)
filename1 = Entry(window, width=40, textvariable = files).grid(column=1, row=0)
selete1 = Button(window, text="选择告警文件",command = selectalarm).grid(column=2, row=0)

label2 = Label(window, text="跳过行数 ").grid(column=0, row=2)

text1 = Text(window,height = 10, width=60).grid(column=1, row=3)
window.mainloop()