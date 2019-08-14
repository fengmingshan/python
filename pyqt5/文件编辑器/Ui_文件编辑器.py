# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\_python\python\pyqt5\文件编辑器.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(631, 369)
		self.centralWidget = QtWidgets.QWidget(MainWindow)
		self.centralWidget.setObjectName("centralWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
		self.gridLayout.setObjectName("gridLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.horizontalLayout.addLayout(self.horizontalLayout_2)
		self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
		self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
		self.textBrowser.setObjectName("textBrowser")
		self.gridLayout.addWidget(self.textBrowser, 0, 1, 2, 1)
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem)
		self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
		self.pushButton_2.setObjectName("pushButton_2")
		self.verticalLayout.addWidget(self.pushButton_2)
		spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem1)
		self.pushButton = QtWidgets.QPushButton(self.centralWidget)
		self.pushButton.setObjectName("pushButton")
		self.verticalLayout.addWidget(self.pushButton)
		spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem2)
		self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
		self.pushButton_3.setObjectName("pushButton_3")
		self.verticalLayout.addWidget(self.pushButton_3)
		spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem3)
		self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_2.addItem(spacerItem4)
		self.gridLayout.addLayout(self.verticalLayout_2, 1, 2, 1, 1)
		MainWindow.setCentralWidget(self.centralWidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.pushButton_2.clicked.connect(self.openfile)
		self.pushButton.clicked.connect(self.choicefont)
		self.pushButton_3.clicked.connect(self.choicecolor)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.pushButton_2.setText(_translate("MainWindow", "打开文件"))
		self.pushButton.setText(_translate("MainWindow", "选择字体"))
		self.pushButton_3.setText(_translate("MainWindow", "选择颜色"))

	def openfile(self):
		fname = QtWidgets.QFileDialog.getOpenFileName(None,'打开文件','./',("Text (*.txt *.log *.py)"))
		if fname[0]:
			 with open(fname[0], 'r',encoding='gb18030',errors='ignore') as f:
				  self.textBrowser.append('打开文件成功')
				  self.textBrowser.append('=======================')
				  self.textBrowser.append(f.read())
	def choicefont(self):
		font, ok = QtWidgets.QFontDialog.getFont()
		if ok:
			self.textBrowser.setCurrentFont(font)
	def choicecolor(self):
		col = QtWidgets.QColorDialog.getColor()
		if col.isValid():
			self.textBrowser.setTextColor(col)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())



if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

