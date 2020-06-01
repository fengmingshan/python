# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:04:09 2020

@author: Administrator
"""

#导出模块
import PySimpleGUI as sg
import time
import inspect
from progress.bar import IncrementalBar

#-----------登录界面，第1个窗口------------
def Denglu(): #登录界面，第1个窗口
    layout = [
              [sg.Text('账号：'),sg.Input(size=(20,1),key=('k1'))],
              [sg.Text('密码：'),sg.Input(size=(20,1),key=('k2'),password_char='*')],
              [sg.Submit(),sg.Cancel()],
             ]

    window = sg.Window('登录界面', layout)
    event, values = window.read()

    while True:
        if event == 'Cancel' or event == None: #成功
            window.close()
            break
        elif event =='Submit':
            if values['k1']=='admin' and values['k2']=='123':
            #这是指定账号和密码的，如果注册后，再从注册后的txt中调出，来判断？
                   sg.Popup('登录成功！')
                   window.close()
                   ZhuMain()

                   break
            else:
               sg.Popup('请输入正确的账号和密码，否则退出。')
               break

    window.close()

#-------------定义进度条的代码及函数-----------

#---定义函数：进度条1---
def Pb1():   #Pb=progress bar=进度条
    import time
    from progress.bar import IncrementalBar

    mylist = [1,2,3,4,5,6,7,8]
    bar = IncrementalBar('进度条1', max = len(mylist)) #len是测列表数据的个数，8个

    for item in mylist:
        bar.next()
        time.sleep(0.1) #延迟时间，0.1~1，之间比较好

    bar.finish()

#---定义函数：进度条2---
def Pb2():
    from progress.bar import Bar
    import time

    bar = Bar('Loading', fill='~', suffix='%(percent)d%%') #fill里面可以填充自己喜欢的符号

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

#---定义函数：进度条3---
def Pb3():
    from progress.bar import Bar
    import time

    bar = Bar('进度条3', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

#---定义函数：进度条4---
def Pb4():
    from progress.bar import ChargingBar
    import time

    bar = ChargingBar('进度条4', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

#---定义函数：进度条5---
def Pb5():
    from progress.bar import FillingSquaresBar
    import time

    bar = FillingSquaresBar('进度条5', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

#---定义函数：进度条6---
def Pb6():
    from progress.bar import FillingCirclesBar
    import time

    bar = FillingCirclesBar('进度条6', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

def Pb7():
    from progress.bar import IncrementalBar
    import time

    bar = IncrementalBar('进度条7', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

def Pb8():
    from progress.bar import PixelBar
    import time

    bar = PixelBar('进度条8', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

def Pb9():
    from progress.bar import ShadyBar
    import time

    bar = ShadyBar('进度条9', max=100) #max的值100，可调节

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()


def Pb10():
    from progress.spinner import Spinner
    #from progress.spinner import MoonSpinner
    #from progress.spinner import PieSpinner
    #from progress.spinner import PixelSpinner
    #from progress.spinner import LineSpinner

    import time

    bar = Spinner('进度条10', max=100) #max的值100，可调节
    #bar = MoonSpinner('进度条10', max=100)
    #bar = PieSpinner('进度条10', max=100)
    #bar = PixelSpinner('进度条10', max=100)
    #bar = LineSpinner('进度条10', max=100)

    for i in range(100): #这个也需要适当调节
        bar.next()
        time.sleep(0.1) #延迟时间，可调节，0.1~1之间最佳

    bar.finish()

def Pb11():
    from alive_progress import alive_bar
    import time

    items = range(100)

    with alive_bar(len(items)) as bar:
        for item in items:
            bar()
            time.sleep(0.1)

def Pb12():
    import PySimpleGUI as sg
    import time

    mylist = [1,2,3,4,5,6,7,8]

    for i, item in enumerate(mylist):
        sg.one_line_progress_meter('进度条12', i+1, len(mylist), '-key-')
        time.sleep(1) #时间选择1最好，因为8个有点短


def Pb13(): #经典，整合后出现在GUI界面上
    import PySimpleGUI as sg
    import time

    mylist = [1,2,3,4,5,6,7,8]
    progressbar = [ [sg.ProgressBar(len(mylist), orientation='h', size=(51, 10), key='progressbar')]]
    outputwin = [ [sg.Output(size=(78,20))]]
    layout = [ [sg.Frame('Progress',layout= progressbar)], [sg.Frame('Output', layout = outputwin)], [sg.Submit('Start'),sg.Cancel()]]

    window = sg.Window('Custom Progress Meter', layout)

    progress_bar = window['progressbar']

    while True:
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        elif event=='Start':
            for i,item in enumerate(mylist):
                print(item)
                time.sleep(1)
                progress_bar.UpdateBar(i+1)

    window.close()

# -------------------------------- GUI Starts Here -------------------------------#
# fig = your figure you want to display.  Assumption is that 'fig' holds the      #
#       information to display.                                                   #
# --------------------------------------------------------------------------------#
#主窗口界面设计
def ZhuMain():
    fig_dict = {'进度条1':Pb1,'进度条2':Pb2,'进度条3':Pb3,'进度条4':Pb4,'进度条5':Pb5,
               '进度条6':Pb6,'进度条7':Pb7,'进度条8':Pb8,'进度条9':Pb9,'进度条10':Pb10,
               '进度条11':Pb11,'进度条12':Pb12,'进度条13':Pb13}

    sg.theme('LightGreen') #主题背景设计，默认银河灰

# define the form layout
    listbox_values = list(fig_dict)

    col_listbox = [
               [sg.Listbox(values=listbox_values, enable_events=True, size=(28, len(listbox_values)), key='-LISTBOX-')],
               [sg.Text('★' * 15)],
               [sg.Exit(size=(5, 2))]
              ]

#布局
    layout = [
          [sg.Text('最全进度条及代码整理', font=('current 10'))],
          [sg.Col(col_listbox, pad=(5, (3, 330))),
           sg.MLine(size=(50, 30), pad=(5, (3, 90)), key='-MULTILINE-')] ,#第2行有3个布局

         ]

# create the form and show it without the plot
    window = sg.Window('Python3下的最全的进度条整理', layout, grab_anywhere=False, finalize=True)

# The GUI Event Loop
    while True:
        event, values = window.read()
                # helps greatly when debugging
        if event in (None, 'Exit'):     # if user closed window or clicked Exit button
            break

        choice = values['-LISTBOX-'][0]   # get first listbox item chosen (returned as a list)
        func = fig_dict[choice]   # get function to call from the dictionary
        window['-MULTILINE-'].update(inspect.getsource(func))  # show source code to function in multiline

    window.close()

if __name__ == '__main__':
    Denglu()