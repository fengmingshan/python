# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\_python\python\pyqt5\文件合并工具\文件合并程序.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import logging

def _append_run_path():
    if getattr(sys, 'frozen', False):
        pathlist = []

        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        pathlist.append(sys._MEIPASS)

        # the application exe path
        _main_app_path = os.path.dirname(sys.executable)
        pathlist.append(_main_app_path)

        # append to system path enviroment
        os.environ["PATH"] += os.pathsep + os.pathsep.join(pathlist)

    logging.error("current PATH: %s", os.environ['PATH'])
_append_run_path()

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget,QFileDialog
from pandas import ExcelWriter,DataFrame,read_excel,read_csv
from os import startfile

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 453)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.verticalLayout_8)
        self.gridLayout.addLayout(self.verticalLayout, 0, 3, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.centralWidget)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_3.addWidget(self.spinBox)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.radioButton1 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton1.setObjectName("radioButton1")
        self.buttonGroup1 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup1.setObjectName("buttonGroup1")
        self.buttonGroup1.addButton(self.radioButton1,1)
        self.verticalLayout_4.addWidget(self.radioButton1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.buttonGroup1.addButton(self.radioButton_2,2)
        self.verticalLayout_4.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.buttonGroup1.addButton(self.radioButton_3,3)
        self.verticalLayout_4.addWidget(self.radioButton_3)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.buttonGroup1.buttonClicked.connect(self.radioButton_clicked)
        self.pushButton.clicked.connect(self.select_file)
        self.pushButton_2.clicked.connect(self.merge_file)
        self.pushButton_3.clicked.connect(self.open_result)
        self.spinBox.valueChanged.connect(self.spinBox_changevalue)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "选择文件"))
        self.pushButton_2.setText(_translate("MainWindow", "合并文件"))
        self.pushButton_3.setText(_translate("MainWindow", "打开结果目录"))
        self.label.setText(_translate("MainWindow", "跳过行数"))
        self.label_2.setText(_translate("MainWindow", "选择文件类型"))
        self.radioButton1.setText(_translate("MainWindow", "EXCEL文件"))
        self.radioButton_2.setText(_translate("MainWindow", "csv文件"))
        self.radioButton_3.setText(_translate("MainWindow", "TXT文件"))

    skip_rows = 0
    def spinBox_changevalue(self,value):
        self.skip_rows = value
        self.textBrowser.append('跳过{0}行'.format(self.skip_rows))

    file_type = ''
    def radioButton_clicked(self):
        sender = self.sender()
        if sender == self.buttonGroup1:
            if self.buttonGroup1.checkedId() == 1:
                Ui_MainWindow.file_type = 'excel'
            elif self.buttonGroup1.checkedId() == 2:
                Ui_MainWindow.file_type = 'csv'
            elif self.buttonGroup1.checkedId() == 3:
                Ui_MainWindow.file_type = 'txt'
            else:
                Ui_MainWindow.file_type = ''

    def select_file(self):
        self.fname = ''
        if Ui_MainWindow.file_type == 'excel':
            self.fname,filetype  = QFileDialog.getOpenFileNames(None,
                                     '打开多个文件',
                                     'D:/',
                                     ("excel (*.xls *.xlsx )"))
        elif Ui_MainWindow.file_type == 'csv':
            self.fname,filetype  = QFileDialog.getOpenFileNames(None,
                                     '打开多个文件',
                                     'D:/',
                                     ("csv (*.csv)"))
        elif Ui_MainWindow.file_type == 'txt':
            self.fname,filetype  = QFileDialog.getOpenFileNames(None,
                                     '打开多个文件',
                                     'D:/',
                                     ("Text (*.txt *.log )"))
        else :
            self.textBrowser.append('未选择文件类型！')
            self.textBrowser.append('=======================')

        try:
            if self.fname[0]:
                self.textBrowser.append('选择{0}个文件'.format(len(self.fname)))
                for file in self.fname:
                    self.textBrowser.append(file)
                self.textBrowser.append('=======================')
        except :
            self.textBrowser.append('请先选择文件类型')
            self.textBrowser.append('=======================')

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

    def get_file_suffix(self,fname):
        if isinstance(fname,list):
            file_suffix = fname[0].split('.')[1]
        else:
            file_suffix = fname.split('.')[1]
        return file_suffix

    def merge_excel(self,fname):
        df_merge = DataFrame()
        if isinstance(fname,list):
            for file in fname:
                df_tmp = read_excel(file,skiprows = self.skip_rows)
                df_merge = df_merge.append(df_tmp)
        else :
            df_merge = read_excel(fname,skiprows = self.skip_rows)
        file_path = self.get_file_path(fname)
        with ExcelWriter(file_path + '合并后文件'+ '.xlsx') as writer:
            df_merge.to_excel(writer,'合并后',index = False)

    def merge_csv(self,fname):
        df_merge = DataFrame()
        if isinstance(fname,list):
            for file in fname:
                df_tmp = read_csv(file, engine = 'python')
                df_merge = df_merge.append(df_tmp)
        else :
            df_merge = read_csv(fname, engine = 'python')
        file_path = self.get_file_path(fname)
        with open(file_path + '合并后文件'+ '.csv','w') as writer:
            df_merge.to_csv(writer,index = False)

    def merge_txt(self,fname):
        content_all = ''
        if isinstance(fname,list):
            for file in fname:
                file_tmp = open(file)
                content = file_tmp.read()
                content_all = content_all + content  + '\n'
        else :
            file_tmp = open(fname)
            content = file_tmp.read()
        file_path = self.get_file_path(fname)
        with open(file_path + '合并后文件'+ '.txt','w') as File:
            File.write(content_all)

    def merge_file(self):
        if  self.fname:
            file_suffix = self.get_file_suffix(self.fname)
            if file_suffix =='xls' or file_suffix =='xlsx':
                self.merge_excel(self.fname)
            elif file_suffix =='csv':
                self.merge_csv(self.fname)
            elif file_suffix =='txt':
                self.merge_txt(self.fname)
            self.textBrowser.append('合并文件成功')
        else:
            self.textBrowser.append('未选择任何文件')
            self.textBrowser.append('=======================')


    def open_result(self):
        result_path = self.get_file_path(self.fname)
        startfile(result_path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
