#含有pandas库的容易报错，需要加以下参数
pyinstaller --clean --win-private-assemblies -F MR.py
pyinstaller --clean --win-private-assemblies -F MR-win.py

pyinstaller --clean --win-private-assemblies -F CQI_LC.py

pyinstaller -F -c -i GRAPH.ICO Ui_文件编辑器.py

# =============================================================================
# 打包pyqt程序运行时报错，添加--hidden-import PyQt5.sip
# =============================================================================
pyinstaller --hidden-import PyQt5.sip -F -w -i GRAPH.ICO Ui_文件编辑器.py


pyinstaller --hidden-import PyQt5.sip -F -w -i warning.ico Ui_Alarm.py

cd D:\test\

