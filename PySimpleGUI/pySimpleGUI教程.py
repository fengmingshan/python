# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:25:49 2020

@author: Administrator
"""

import PySimpleGUI as sg

def 总体说明():
    #下面这个layout变量就是控件的集合,里面放空间
    #将来我们直接把这个变量传到窗口(屏幕)那里
    #你可以把它当作实际内容
    #以下是个简单的例子
    layout = [[sg.Text("要显示在窗口上的文字")], [sg.Button("完成")]]
    #他还有参数,你懂的:title='Options',etitle_color='rd',

    #sg.Window(),创建一个窗口,第一个参数是窗口名称,有latout参数就是本窗口的内容
    window1 = sg.Window("Jarvis",layout=layout)
    #可以设置no_titlebar=True就没有边框了,而且不会显示图标(暂时不清楚是怎么回事)
	#还有个类似的:form = sg.FlexForm('Everything bagel', default_element_size=(40, 1))

    #上面那种方式是在构造的时候就传入内容,我们也可以在后面调用window对象 的Layout()方法,参数就是你要传入的内容
    window1.Layout(layout)

    # Read()是阻塞式方法,会阻塞程序的进行，直到Button被点击才有返回值
    button, value = window1.Read()
    #返回一个元组,
    #元组的第一个元素就是按钮的名称(字符串类型,你在layout那里填的)
    print('button:', button)
    #第二个元素是字典,返回字典，所有可输入,可选择的值.键是由零开始的索引,值就看你设置的value了

    print('value:', value)

def 排版_基本排列():

#排版说明,
#对于layout列表来说,它是一个二维列表
#第一维德元素分居不同的行上,第二维度上的元素们居于同一行,不同列上
#[ [(0,0),(0,1),(0,2)]
#  [(1,0),(1,1),(1,2),(1,3),......]
#  [(2,0),(2,1),(2,2),]
# ]
	layout = [
		[sg.Text('Please enter your Name, Address, Phone')],
		[sg.Text('Name', size=(15, 1)), sg.InputText('name')],
		[sg.Text('Address', size=(15, 1)), sg.InputText('address')],
		[sg.Text('Phone', size=(15, 1)), sg.InputText('phone')],
		[sg.Submit(), sg.Cancel()]
	]

	window = sg.Window('window titel', layout=layout)

	button, values = window.read()

	print(button, values[0], values[1], values[2])

def 排版_框架():
    #这个Frame组件很像HTML中的那个,
    #用来实现layout的嵌套
    child_layout = [[sg.Text('第一行')], [sg.Text('第二行')]]

    layout = [

        [sg.Text('第一行'), sg.Frame('标题', child_layout)]
    ]

    window = sg.Window('框架组件').Layout(layout)

    button, value = window.Read()

    print('button:', button)

    print('value:', value)

def 排版_目录():
    #主要就是那个sg.Menu()
    #具体的参数格式,方法调用一看就明白了,不再赘述
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['Help', 'About...'], ]
    layout = [[sg.Menu(menu_def, tearoff=True)]]
    window = sg.Window('目录演示', default_element_size=(40, 1), grab_anywhere=True).Layout(layout)
    event, values = window.Read()

def 右键目录():
    #有的控件有这个属性比如right_click_menu=['UNUSED', 'Exit'])]
    #和目录一样操作就好了
    pass

def 控件():

    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],['&Help', '&About...'], ]

    # ------ Column Definition ------ #

#当较小的元素左侧有一个较高的元素时，则需要一列。
    #将来也放到layout的一个控件里面sg.Column(col, background_color='blue')
    column1 = [[sg.Text('Column 1', justification='center', size=(10, 1))],
[sg.Spin(values=('Spin Box 1', '2', '3'),initial_value='Spin Box 1')],
[sg.Spin(values=('Spin Box 1', '2', '3'),initial_value='Spin Box 2')],
[sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

    layout = [

        [sg.Menu(menu_def, tearoff=True)],

        #文本显示内容,那个relief参数可以添加阴影效果
        #sg.RELIEF_RIDGE,RELIEF_RAISED为外凸效果
        #sg.RELIEF_FLAT平滑效果,也就是默认值
        #RELIEF_GROOVE,sg.RELIEF_SUNKEN内凹效果
        #RELIEF_SOLID黑框选中
        [sg.Text('(Almost) All widgets in one Window!', size=(
        30, 1), justification='center', font=("Helvetica", 25),relief=sg.RELIEF_RIDGE)],

        [sg.Text('Here is some text.... and a place to enter text')],

        # 单行文本输入框
        [sg.InputText('This is my text')],

        #框架组件,之前说过
        [sg.Frame(layout=[
            #复选框,将来valuse的返回值只有False,True
            [sg.CBox('这里输什么将来就显示什么', size=(10, 1)),
            sg.CBox('My second checkbox!', default=True)],

            #这里是单选框,第一个参数是实际显示值,第二个是id,这个只要学过HTML的都懂吧
            [sg.Radio('My first Radio!     ', "123",default=True, size=(10, 1)),
            sg.Radio('My second Radio!', "123")]], title='Options', relief=sg.RELIEF_SUNKEN,
            tooltip='Use these to set flags')],

        #这个是多行输入框
        [sg.MLine(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),
        sg.MLine(default_text='A second multi-line', size=(35, 3))],

        #这个是多选一框(好像叫selectbox),就是那种选择出身年份的,name和value都很好懂
        [sg.Combo(('Combobox 1', 'Combobox 2'), default_value='Combobox 1', size=(20, 1)),

        #用来滑动的条,你可以选择滑动条的范围,方向"h"/"v",尺寸,默认值
         #实际值就是你拖动的结果
         sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],

        #不知道是个啥,跟上面那个Combo很像
        [sg.OptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))],

        #就是你平时用browse实际出来的那个有拖动条的那种
        #功能上跟Combo很像
        [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3))],

       #可以画线,还可以展位(用" ")
        [sg.Text('_' * 100)],

        #File选择器,值就是你选中的File的路径
         [ sg.FolderBrowse()],

        #快捷方式按钮,还有提示tooltip就是你把光标移动到控件旁边后会提示的小白色的提示框
        [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]]

    window = sg.Window('Everything bagel', layout,
                       no_titlebar=True,
                       default_element_size=(40, 1),
                       grab_anywhere=False,
                       )
    event, values = window.read()

def 图片():
    #我知道有这么一个sg.Image控件,但用的时候总是报错
    layout=[sg.Image(
        size=(10,10)
        ,filename=r"D:\python-related\workspace\p7-Jarvis\prepare\btn_screenshot_prev_down.png")]
    window=sg.Window(layout)
    #a=window.read()


def 标签():
    tab1_layout = [[sg.Text('This is inside tab 1')]]

    tab2_layout = [[sg.Text('This is inside tab 2')],
                   [sg.In(key='in')]]

    layout = [
        [sg.TabGroup([[sg.Tab('Tab 1', tab1_layout, tooltip='tip'), sg.Tab('Tab 2', tab2_layout)]], tooltip='TIP2')],
        [sg.Button('Read')]]

    window = sg.Window('My window with tabs', layout, default_element_size=(12, 1))

    while True:
        event, values = window.read()
        print(event, values)
        if event is None:  # always,  always give a way out!
            break

def 轮询():
    #window的read()方法是个阻塞式方法,如果就是不安按钮就等下去,
    #那么你在按按钮之前是没法更新的
    #所以就有了轮询操作
    #read()方法不再是阻塞式方法了,
    #设置timeout参数之后,每隔一定事件之后就自动获取event 和values

    #这里有个小bug(sg库的),就是你要更新Text控件的时候,
    #记得在构造的时候就把它的长度设置的长一点(比如" "*100),
    #否则将来你的Text控件只能显示输入框的第一个字

    # if event == sg.TIMEOUT_KEY:
    #     print("Nothing happened")
    layout=[
        [sg.Text(" "*85,key="text")],
        [sg.Input(key="input")]
    ]
    window=sg.Window(title="轮询",layout=layout)
    while True:
        event,values=window.read(timeout=10)
        print(values)
        window["text"].update(values["input"])
        if event in (None,"Exit"):
            window.close()

def 外观优化_主题配色():
    # 外观
    #sg.preview_all_look_and_feel_themes()
    # print(sg.ListOfLookAndFeelValues())
    # ['SystemDefault', 'Reddit', 'Topanga', 'GreenTan', 'Dark', 'LightGreen', 'Dark2', 'Black', 'Tan', 'TanBlue',
    # 'DarkTanBlue', 'DarkAmber', 'DarkBlue', 'Reds', 'Green', 'BluePurple', 'Purple', 'BlueMono', 'GreenMono',
    # 'BrownBlue', 'BrightColors', 'NeutralBlue', 'Kayak', 'SandyBeach', 'TealMono']
    # 改变风格(包括按钮,背景颜色的调色方案)的方法.
    #sg.theme(new_theme)

    #还有一个另外的,你可以在下面的外观优化_自定义图标_二里看到效果
    #background = '#F0F0F0'
    #sg.SetOptions(background_color=background, element_background_color=background)
    ##要设置背景和按钮的背景相同,经过这个设置后会产生诡异的效果
        #甚至可能比单纯设置sg.theme()还好


    def sample_layout():
        return [[sg.Text('Text element'), sg.InputText('Input data here', size=(12, 1))],
                [sg.Button('Ok'), sg.Button('Cancel')]]

    layout = [[sg.Text('My Theme Previewer', font='Default 18', background_color='black',)]]

    row = []
    for count, theme in enumerate(sg.theme_list()):
        sg.theme(theme)
        if not count % 10:
            layout += [row]
            row = []
        row += [sg.Frame(theme, sample_layout())]
    if row:
        layout += [row]
    sg.Window('Window Title', layout, background_color="black",grab_anywhere=True).read()

def 外观优化_透明度():
    #外观优化还有个方法是去掉标题栏,那个在第一个介绍中已经说明了
    #这里都是通过设置属性实现的
    layout = [
        [sg.Text('Please enter your Name, Address, Phone')],
        [sg.Text('Name', size=(15, 1)), sg.InputText('name')],
        [sg.Text('Address', size=(15, 1)), sg.InputText('address')],
        [sg.Text('Phone', size=(15, 1)), sg.InputText('phone')],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('PSG System Dashboard', layout, no_titlebar=True, alpha_channel=.5, grab_anywhere=True)
    button, values = window.read()

def 外观优化_自定义图标_一():
      #1
    #要把图片变成一种basic64的格式,提供一个网站:
    #https://base64.guru/converter/encode/image
    #然后在构造按钮的时候把它传给参数image_data就好
    #2
      #你的图片可能很大,所以还要调整image_subsample这个参数来调整按钮图片的大小
    #3
      #就算你的png图片已经扣掉了背景,但显示起来还是有问题
      #所以要设置Button的一个属性为button_color=('white',sg.theme_background_color())
      #都是死的,至于那个"white"我换成其他颜色暂时没问题
    red_x_base64 =b'R0lGODlhoAAUAIAAAAQCBP7+/iH/C05FVFND'
    layout = [[sg.Text('My borderless window with a button graphic')],
                [sg.Button('', image_data=red_x_base64, button_color=("white",sg.theme_background_color()), border_width=0,
                           image_subsample=8, key='Exit')]]


    window = sg.Window('Window Title', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event in (None, 'Exit'):
            break
    window.close()

def 外观优化_自定义图标_二():
    #这个方法比上一个方便一点,
    #直接加载图片就好
    #主要是设置Button的image_filename属性

    def MediaPlayerGUI():
        background = '#F0F0F0'
        #要设置背景和按钮的背景相同,经过这个设置后会产生诡异的效果
        #甚至可能比单纯设置sg.theme()还好
        sg.SetOptions(background_color=background, element_background_color=background)
        随便找的图片=r"D:\python-related\workspace\p7-Jarvis\prepare\btn_screenshot_prev_down.png"
        image_pause = 随便找的图片
        image_restart = 随便找的图片
        image_next = 随便找的图片
        image_exit =随便找的图片


        # define layout of the rows
        layout = [[sg.Text('Media File Player', size=(17, 1), font=("Helvetica", 25))],
                  [sg.Text(size=(15, 2), font=("Helvetica", 14), key='output')],
                  [sg.Button('', button_color=(background, background),
                             image_filename=image_restart, image_size=(50, 50), image_subsample=2, border_width=0,
                             key='Restart Song'),
                   sg.Text(' ' * 2),
                   sg.Button('', button_color=(background, background),
                             image_filename=image_pause, image_size=(50, 50), image_subsample=2, border_width=0,
                             key='Pause'),
                   sg.Text(' ' * 2),
                   sg.Button('', button_color=(background, background), image_filename=image_next, image_size=(50, 50),
                             image_subsample=2, border_width=0, key='Next'),
                   sg.Text(' ' * 2),
                   sg.Text(' ' * 2), sg.Button('', button_color=(background, background),
                                               image_filename=image_exit, image_size=(50, 50), image_subsample=2,
                                               border_width=0, key='Exit')],
                  [sg.Text('_' * 20)],
                  [sg.Text(' ' * 30)],
                  [
                      sg.Slider(range=(-10, 10), default_value=0, size=(10, 20), orientation='vertical',
                                font=("Helvetica", 15)),
                      sg.Text(' ' * 2),
                      sg.Slider(range=(-10, 10), default_value=0, size=(10, 20), orientation='vertical',
                                font=("Helvetica", 15)),
                      sg.Text(' ' * 2),
                      sg.Slider(range=(-10, 10), default_value=0, size=(10, 20), orientation='vertical',
                                font=("Helvetica", 15))],
                  [sg.Text('   Bass', font=("Helvetica", 15), size=(9, 1)),
                   sg.Text('Treble', font=("Helvetica", 15), size=(7, 1)),
                   sg.Text('Volume', font=("Helvetica", 15), size=(7, 1))]
                  ]

        # Open a form, note that context manager can't be used generally speaking for async forms
        window = sg.Window('Media File Player', layout, default_element_size=(20, 1),
                           font=("Helvetica", 25))
        # Our event loop
        while (True):
            event, values = window.read(timeout=100)  # Poll every 100 ms
            if event == 'Exit' or event is None:
                break
            # If a button was pressed, display it on the GUI by updating the text element
            if event != sg.TIMEOUT_KEY:
                window['output'].update(event)

    MediaPlayerGUI()

def 外观优化_按钮紧密布局():
#要看的核心代码sg.SetOptions(element_padding=(0, 0))
#剩下的随便看看
    """
    演示如何使用深色主题的“紧密”布局。
     显示用户应用程序如何控制按钮状态。 该程序管理禁用/启用
     按钮的状态并更改文本颜色以显示灰色（禁用）按钮 """

    sg.ChangeLookAndFeel('Dark')
    sg.SetOptions(element_padding=(0, 0))

    layout = [
        [sg.T('User:', pad=((3, 0), 0)), sg.OptionMenu(values=('User 1', 'User 2'), size=(20, 1)),
         sg.T('0', size=(8, 1))],
        [sg.T('Customer:', pad=((3, 0), 0)), sg.OptionMenu(values=('Customer 1', 'Customer 2'), size=(20, 1)),
         sg.T('1', size=(8, 1))],
        [sg.T('Notes:', pad=((3, 0), 0)), sg.In(size=(44, 1), background_color='white', text_color='black')],
        [sg.Button('Start', button_color=('white', 'black'), key='Start'),
         sg.Button('Stop', button_color=('white', 'black'), key='Stop'),
         sg.Button('Reset', button_color=('white', 'firebrick3'), key='Reset'),
         sg.Button('Submit', button_color=('white', 'springgreen4'), key='Submit')]
    ]

    window = sg.Window("Time Tracker", layout, default_element_size=(12, 1), text_justification='r',
                       auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1))
    window.Finalize()
    window['Stop'].update(disabled=True)
    window['Reset'].update(disabled=True)
    window['Submit'].update(disabled=True)
    recording = have_data = False
    while True:
        event, values = window.read()
        print(event)
        if event is None:
            exit(69)
        if event == 'Start':
            window['Start'].update(disabled=True)
            window['Stop'].update(disabled=False)
            window['Reset'].update(disabled=False)
            window['Submit'].update(disabled=True)
            recording = True
        elif event == 'Stop' and recording:
            window['Stop'].update(disabled=True)
            window['Start'].update(disabled=False)
            window['Submit'].update(disabled=False)
            recording = False
            have_data = True
        elif event == 'Reset':
            window['Stop'].update(disabled=True)
            window['Start'].update(disabled=False)
            window['Submit'].update(disabled=True)
            window['Reset'].update(disabled=False)
            recording = False
            have_data = False
        elif event == 'Submit' and have_data:
            window['Stop'].update(disabled=True)
            window['Start'].update(disabled=False)
            window['Submit'].update(disabled=True)
            window['Reset'].update(disabled=False)
            recording = False

def 外观优化_页边距():
    #把控件和窗口的距离减小有时候也可以美化应用
    #这个是去设置window的参数margins=(0,0),
    #这个我就懒的做例子了
    #你随便找一个试试就好
    pass

def 外观优化_更多参数():
    #其实上面说的那些优化手段大多是通过设置Window参数来实现的
    #它的参数还有很多,在这里就是全部的参数及其默认项
    # icon = None
    # button_color = (None, None)
    # element_size = (None, None),
    # margins = (None, None),
    # element_padding = (None, None)
    # auto_size_text = None
    # auto_size_buttons = None
    # font = None
    # border_width = None
    # slider_border_width = None
    # slider_relief = None
    # slider_orientation = None
    # autoclose_time = None
    # message_box_line_width = None
    # progress_meter_border_depth = None
    # progress_meter_style = None
    # progress_meter_relief = None
    # progress_meter_color = None
    # progress_meter_size = None
    # text_justification = None
    # text_color = None
    # background_color = None
    # element_background_color = None
    # text_element_background_color = None
    # input_elements_background_color = None
    # element_text_color = None
    # input_text_color = None
    # scrollbar_color=None, text_color=None
    # debug_win_size = (None, None)
    # window_location = (None, None)
    # tooltip_time = None
    pass

def values优化():
    '''在之前你想要获取输入值,就只能数它的位置,然后values[索引]
    但是这个数字索引用起来有点不方便,我们有一种更简单的,获取该输入值的方法,
    就是在构建这个控件的时候就自定义一个键,将来直接对values字典使用这个键就OK'''
    layout = [[sg.Text('My one-shot window.')],
              [sg.InputText(key='-IN-')],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Window Title', layout)

    event, values = window.read()
    window.close()

    text_input = values['-IN-']
    sg.popup('You entered', text_input)

def 找到元素():
    #学过JS的多知道一点dom,bom吧,它们有一个就是为了获得标签元素
     #这个GUI库里面也有方法返回元素
     #window[元素的key],window.FindElement('元素的key).window.Element(元素的key)
    #这个例子中还用了个update方法,不过我暂时不太感兴趣
    layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15, 1), key='-OUTPUT-')],
              [sg.Input(key='-IN-')],
              [sg.Button('Show'), sg.Button('Exit')]]

    window = sg.Window('Pattern 2B', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event in (None, 'Exit'):
            break
        if event == 'Show':
            # Update the "output" text element to be the value of "input" element
            window['-OUTPUT-'].update(values['-IN-'])

    window.close()

def 网格风的按钮():
    #妙啊
    #那个window[event]和update()的用法还没太看明白
    from random import randint

    MAX_ROWS = MAX_COL = 10
    board = [[randint(0, 1) for j in range(MAX_COL)] for i in range(MAX_ROWS)]

    layout = [[sg.Button('?', size=(4, 2), key=(i, j), pad=(0, 0)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]

    window = sg.Window('Minesweeper', layout,margins=(0,0))

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        # window[(row, col)].update('New text')   # To change a button's text, use this pattern
        # For this example, change the text of the button to the board's value and turn color black
        window[event].update(board[event[0]][event[1]], button_color=('white', 'black'))
    window.close()

def 任务匹配器_及其他事件类型():
    #基本的监听任务机制我在前面的一篇博客里说的比较清楚了,
    #这里只是感觉它有几个亮点

    # 除了键盘的点击事件,还可以添加其他类型的事件
    # 但我实在懒得弄了,等用到再说吧
    """Layout的read方法会等待用户进行响应，称为blocking event，分为三种情况：
    第一种响应是按钮点击响应。每次用户点击按钮后，会返回两个值，一个是按钮的名称，一个是返回值。返回值是字典的形式，key是部件name，value是对应的值。
    第二种响应是Enter响应。在属性中设置change_submits = True即可，这样按下Enter键就会触发响应。
    第三种响应是鼠标/键盘事件。在属性中设置return_keyboard_events = True即可。"""

    sg.theme('Light Blue 3')

    # The callback functions
    def button1():
        print('Button 1 callback')

    def button2():
        print('Button 2 callback')

    # Lookup dictionary that maps button to function to call
    dispatch_dictionary = {'1': button1, '2': button2}

    # Layout the design of the GUI
    layout = [[sg.Text('Please click a button', auto_size_text=True)],
              [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Quit()]]

    # Show the Window to the user
    window = sg.Window('Button callback example', layout)

    # Event loop. Read buttons, make callbacks
    while True:
        # Read the Window
        event, value = window.read()
        if event in ('Quit', None):
            break

#就是这里,这种调用方式很不错
        # Lookup event in function dictionary
        if event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]  # get function from dispatch dictionary
            func_to_call()
        else:
            print('Event {} not in dispatch dictionary'.format(event))

    window.close()

    # All done!
    sg.popup_ok('Done')

def 计时器_伪():
    sg.theme('DarkBrown1')
    layout = [[sg.Text('', size=(10, 2), font=('Helvetica', 20), justification='center', key='_OUTPUT_')],
              #这个用空格占位很不错
              [sg.T(' ' * 5), sg.Button('Start/Stop', focus=True), sg.Quit()]]
    window = sg.Window('Stopwatch Timer', layout)
    timer_running, counter = True, 0
    #上面的都好说

    while True:
        event, values = window.read(timeout=10)  # Please try and use as high of a timeout value as you can
        if event in (None, 'Quit'):  # if user closed the window using X or clicked Quit button
            break
        elif event == 'Start/Stop':
            timer_running = not timer_running
        if timer_running:
            window['_OUTPUT_'].update(
                '{:02d}:{:02d}.{:02d}'.format((counter // 100) // 60, (counter // 100) % 60, counter % 100))
            counter += 1
        #这么看来,是通过计数和运算实现的,
        #我还以为这是个什么控件,再不济也用了个什么控件

def 计时器_完美():
    import time
    #这个案例中有很多值得借鉴的东西
    #比如
    '''
    sg.ChangeLookAndFeel('Black')
    sg.SetOptions(element_padding=(0, 0))
    sg.Button('Pause', key='button', button_color=('white', '#001480')
    window = sg.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                       grab_anywhere=True)'''


    """
     计时器桌面小部件创建一个始终位于其他窗口顶部的浮动计时器可以通过抓住窗口上的任意位置来移动它，该示例很好地说明了如何使用SimpleGUI进行无阻塞的轮询程序，可在Pi上运行时用于轮询硬件
      当计时器刻度是由PySimpleGUI的“超时”机制生成时，实际值
       显示的计时器的一部分来自系统计时器time.time（）。 这保证了
       无论PySimpleGUI计时器刻度的准确性如何，都会显示准确的时间值。 如果
       如果不使用此设计，则显示的时间值将缓慢偏移时间
       它需要执行PySimpleGUI读取和更新调用（不好！）
      注意-使用退出按钮退出时，您会得到一条警告消息。
      它将类似于：无效的命令名称\“ 1616802625480StopMove \”
    """

    # ----------------  Create Form  ----------------
    sg.ChangeLookAndFeel('Black')
    sg.SetOptions(element_padding=(0, 0))

    layout = [[sg.Text('')],
              [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],
              [sg.Button('Pause', key='button', button_color=('white', '#001480')),
               sg.Button('Reset', button_color=('white', '#007339'), key='Reset'),
               sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]

    window = sg.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                       grab_anywhere=True)

    # ----------------  main loop  ----------------
    current_time = 0
    paused = False
    start_time = int(round(time.time() * 100))
    while (True):
        # --------- Read and update window --------
        if not paused:
            event, values = window.read(timeout=10)
            current_time = int(round(time.time() * 100)) - start_time
        else:
            event, values = window.read()
        if event == 'button':
            event = window[event].GetText()
        # --------- Do Button Operations --------
        if event is None or event == 'Exit':  # ALWAYS give a way out of program
            break
        if event == 'Reset':
            start_time = int(round(time.time() * 100))
            current_time = 0
            paused_time = start_time
        elif event == 'Pause':
            paused = True
            paused_time = int(round(time.time() * 100))
            element = window['button']
            element.update(text='Run')
        elif event == 'Run':
            paused = False
            start_time = start_time + int(round(time.time() * 100)) - paused_time
            element = window['button']
            element.update(text='Pause')

        # --------- Display timer in window --------
        window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                            (current_time // 100) % 60,
                                                            current_time % 100))

def 简单进度条():
    #和计时器不同,这个用到了新的控件
    sg.theme('Dark Blue 8')

    for i in range(10000):
        sg.OneLineProgressMeter('One Line Meter Example', i + 0.1, 10000, 'key')

def 自定义进度条():
    #上面那个进度条,方向(横竖),尺寸,都是确定的,而且旁边还有一些复杂的参数
    #下面这个就相对灵活很多
    #具体用法多看两眼就懂了

    # layout the Window
    layout = [[sg.Text('A custom progress meter')],
              [sg.ProgressBar(10000, orientation='v', size=(40, 40), key='progbar')],
              [sg.Cancel()]]

    # create the Window
    window = sg.Window('Custom Progress Meter', layout)
    # loop that would normally do something useful
    for i in range(10000):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)
        if event == 'Cancel' or event is None:
            break
            # update bar with loop value +1 so that bar eventually reaches the maximum
        window['progbar'].update_bar(i + 0.1)
    # done with loop... need to destroy the window as it's still open
    window.close()

def 多窗口_隐藏():
    #其实也没啥难的,只要在某个按钮事件添加打开新窗口就好
    #主要是看两个方法:
    #window.Hide(),window.Unhide()

    layout = [[sg.Text('Window 1'), ],
              [sg.Input()],
              [sg.Text('', key='_OUTPUT_')],
              [sg.Button('Launch 2')]]

    win1 = sg.Window('Window 1', layout)
    win2_active = False
    while True:
        ev1, vals1 = win1.Read(timeout=1)
        if ev1 is None:
            break
        win1['_OUTPUT_'].update(vals1[0])

        if ev1 == 'Launch 2' and not win2_active:
            win2_active = True
            win1.Hide()
            layout2 = [[sg.Text('Window 2')], [sg.Button('Exit')]]

            win2 = sg.Window('Window 2', layout2)
            while True:
                ev2, vals2 = win2.Read()
                if ev2 is None or ev2 == 'Exit':
                    win2.Close()
                    win2_active = False
                    win1.UnHide()
                    break

def 与matplotlib结合():
    import matplotlib.pyplot as plt

    """
       同时PySimpleGUI窗口和Matplotlib交互式窗口
         许多人要求运行正常的PySimpleGUI窗口的功能，
         启动与通常的Matplotlib控件交互的MatplotLib窗口。
         事实证明这是一件相当简单的事情。
         秘诀是在plt.show（）中添加参数block = False"""

    def draw_plot():
        plt.plot([0.1, 0.2, 0.5, 0.7])
        plt.show(block=False)

    layout = [[sg.Button('Plot'), sg.Cancel(), sg.Button('Popup')]]

    window = sg.Window('Have some Matplotlib....', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Plot':
            draw_plot()
        elif event == 'Popup':
            sg.popup('Yes, your application is still running')
    window.close()

def CPU利用率():
    import psutil

    # ----------------  Create Window  ----------------
    sg.ChangeLookAndFeel('Black')
    layout = [[sg.Text('')],
              [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],
              [sg.Exit(button_color=('white', 'firebrick4'), pad=((15, 0), 0)),
               sg.Spin([x + 1 for x in range(10)], 1, key='spin')]]

    window = sg.Window('Running Timer', layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                       grab_anywhere=True)

    # ----------------  main loop  ----------------
    while (True):
        # --------- Read and update window --------
        event, values = window.read(timeout=0)

        # --------- Do Button Operations --------
        if event is None or event == 'Exit':
            break
        try:
            interval = int(values['spin'])
        except:
            interval = 1

        cpu_percent = psutil.cpu_percent(interval=interval)

        # --------- Display timer in window --------

        window['text'].update(f'CPU {cpu_percent:02.0f}%')

    # Broke out of main loop. Close the window.
    window.close()

def 其他():
    '''如果使用了多线程,就要这样关闭窗口:window.close()
        del window'''
    pass

#测试区:
#总体说明()
#排版_基本排列()
#排版_框架()
#排版_目录()
#控件()
#图片()
#标签()
#轮询()
#外观优化_主题配色()
#外观优化_透明度()
#外观优化_自定义图标_一()
#外观优化_自定义图标_二()
#外观优化_按钮紧密布局()
#网格风的按钮()
#找到元素()
#任务匹配器_及其他事件类型()
#计时器_伪()
#计时器_完美()
#简单进度条()
#自定义进度条()
#多窗口_隐藏()
#与matplotlib结合()
#CPU利用率()
