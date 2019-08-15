# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\_python\python\pyqt5\爱立信告警统计\爱立信告警统计.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from pandas import ExcelWriter,DataFrame
from os import listdir
from os import startfile
from datetime import datetime
from re import findall
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    fname = []
    data_path = ''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 288)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.open_singlefile)
        self.pushButton_2.clicked.connect(self.open_multifile)
        self.pushButton_3.clicked.connect(self.static_file)
        self.pushButton_4.clicked.connect(self.open_result)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "打开单个文件"))
        self.pushButton_2.setText(_translate("MainWindow", "打开多个文件"))
        self.pushButton_3.setText(_translate("MainWindow", "开始统计"))
        self.pushButton_4.setText(_translate("MainWindow", "打开结果目录"))

    def open_singlefile(self):
        Ui_MainWindow.fname = QtWidgets.QFileDialog.getOpenFileName(None,
                                '打开单个文件',
                                './',
                                ("Text (*.txt *.log)"))
        if Ui_MainWindow.fname[0]:
            self.textBrowser.append('打开1个文件')
            self.textBrowser.append(Ui_MainWindow.fname[0])

    def open_multifile(self):
        Ui_MainWindow.fname,filetype  = QtWidgets.QFileDialog.getOpenFileNames(None,
                                 '打开多个文件',
                                 './',
                                 ("Text (*.txt *.log )"))
        if Ui_MainWindow.fname[0]:
            self.textBrowser.append('打开{0}个文件'.format(len(Ui_MainWindow.fname)))
            for file in Ui_MainWindow.fname:
                self.textBrowser.append(file)

    def static_file(self):
        content_all = ''
        for file in Ui_MainWindow.fname:
            file_tmp = open(file)
            content = file_tmp.read()
            content_all = content_all + content
        self.textBrowser.append('打开文件成功')
        self.textBrowser.append('=======================')
        df_alarm = DataFrame()
        df_alarm['网元'] = ''
        df_alarm['告警名称'] = ''
        df_alarm['告警级别'] = ''
        df_alarm['告警当前状态'] = ''
        df_alarm['发生时间'] = ''
        df_alarm['恢复时间'] = ''
        df_alarm['故障原因'] = ''
        df_alarm['附加信息'] = ''

        alarm_name_dict ={ 'Heartbeat Failure':'基站掉站',
                            'Service Unavailable':'小区服务不可用',
                            'No Connection':'',
                            'RET Failure':'',
                            'RET Not Calibrated':'',
                            'Service Degraded':'小区服务质量下降',
                            'VSWR Over Threshold':'',
                            'Link Failure':'',
                            'Power Loss':'',
                            'TimeSyncIO Reference Failed':'',
                            'Calendar Clock Misaligned':'',
                            'Synchronization End':'',
                            'Synchronization Start':'',
                            'PLMN Service Unavailable':'',
                            'SFP Stability Problem':''}

        alarm_class_dict ={ 'Critical':'紧急告警',
                            'Major':'主要告警',
                            'Minor':'次要告警',
                            'Warning':'警告告警',
                            'Indeterminate':'不确定告警',
                            'Cleared':'已恢复告警'}

        p1 = r'(AlarmId.*[\s\S]+?FDN2:)'  # 正则表达式，匹配一条完整的告警记录文件
        alarm_list = findall(p1,content_all) # 通过正则匹配分割所有的告警记录

        i = 0
        for j in range(0,len(alarm_list)):
             lines = alarm_list[j].split('\n')
             for line in lines:
                  if 'ObjectOfReference:' in line:
                       df_alarm.loc[i,'网元'] = line.split(',')[2].split('=')[1]
                  if 'SpecificProblem:' in line:
                       df_alarm.loc[i,'告警名称'] = line.split(':')[1].replace('\n','')
                  if 'PerceivedSeverity:' in line:
                       df_alarm.loc[i,'告警级别'] = line.split(':')[1].replace('\n','')
                  if 'EventTime:' in line:
                       df_alarm.loc[i,'发生时间'] = line.split('EventTime:')[1].replace('\n','')
                  if 'CeaseTime:' in line:
                       df_alarm.loc[i,'恢复时间'] = line.split('CeaseTime:')[1].replace('\n','')
                  if 'ProbableCause:' in line:
                       df_alarm.loc[i,'故障原因'] = line.split(':')[1].replace('\n','')
                  if 'eriAlarmNObjAdditionalText:' in line:
                       df_alarm.loc[i,'附加信息'] = line.split(':')[1].replace('\n','')
             i +=1

        df_alarm['告警名称'] = df_alarm['告警名称'].map(alarm_name_dict)
        df_alarm['告警级别'] = df_alarm['告警级别'].map(alarm_class_dict)

        current_time = str(datetime.now()).split('.')[0].replace(':','.')

        path_list = Ui_MainWindow.fname[0].split('/')
        del(path_list[-1])
        for name in path_list:
            Ui_MainWindow.data_path = Ui_MainWindow.data_path + name + '\\'
        with ExcelWriter(Ui_MainWindow.data_path + '爱立信当前告警' + current_time + '.xlsx' ) as writer:
            df_alarm.to_excel(writer,'当前告警',index = False)
        self.textBrowser.append('分析完成！')

    def open_result(self):
        startfile(Ui_MainWindow.data_path)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

