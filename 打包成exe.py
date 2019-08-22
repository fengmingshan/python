#含有pandas库的容易报错，需要加以下参数
pyinstaller --clean --win-private-assemblies -F MR.py
pyinstaller --clean --win-private-assemblies -F MR-win.py

pyinstaller --clean --win-private-assemblies -F CQI_LC.py

pyinstaller -F -c -i GRAPH.ICO Ui_文件编辑器.py

# =============================================================================
# 打包pyqt程序运行时报错，添加--hidden-import PyQt5.sip
# =============================================================================
pyinstaller --hidden-import PyQt5.sip -F -w -i "d:\py2exe\file_merge.ico" d:\test\Ui_文件合并程序.py

pyinstaller --hidden-import PyQt5.sip -F -w -i "d:\py2exe\file_merge.ico" --upx "d:\py2exe\upx391w" d:\py2exe\Ui_文件合并程序.py

pyinstaller --hidden-import PyQt5.sip -w -i "d:\py2exe\file_merge.ico" d:\test\Ui_文件合并程序.py

pyinstaller --clean --hidden-import PyQt5.sip -c -i "d:\py2exe\file_merge.ico" d:\test\Ui_文件合并程序.py

pyinstaller --clean --hidden-import PyQt5.sip -F -w -i "d:\py2exe\Warning2.ico" d:\test\Ui_爱立信告警统计.py

pyinstaller --hidden-import PyQt5.sip -F -w -i warning.ico Ericsson_Alarm_Static.py

# =============================================================================
# 参数说明
# =============================================================================
#    -F, --onefile Py代码只有一个文件
#
#    -D, --onedir Py代码放在一个目录中（默认是这个）
#
#    -K, --tk 包含TCL/TK
#
#    -d, --debug 生成debug模式的exe文件
#
#    -w, --windowed, --noconsole 窗体exe文件(Windows Only)
#
#    -c, --nowindowed, --console 控制台exe文件(Windows Only)
#
#    -o DIR, --out=DIR 设置spec文件输出的目录，默认在PyInstaller同目录
#
#    -i/--icon=<FILE.ICO> 加入图标（Windows Only）
#
#    -v FILE, --version=FILE 加入版本信息文件
#
#    --upx-dir, 压缩可执行程序

# =============================================================================
# 减小打包大小
# =============================================================================
#方法1 去除不必要的库
#pyinstaller除了会打包test.py使之成为一个exe之外，还会创建一的后缀名为 .spec 的文件
#
#然后就可以愉快的在第13行的"[]"里面输入自己不需要的库啦
#
#然后输入这样的代码重新打包自己的exe
#pyinstaller --clean -F test.spec
#不嫌麻烦的话一开始也可以这么写：
#pyinstaller --clean -F test.py --exclude-module matplotlib ^ ......(此处省略）
#
#ps：像requests这些库啊 是和urllib有关联的 这也就是为什么 exclude urllib可能会有错误产生


#方法2 虚拟环境
#
#首先呢 我们需要一位名为virtualenv的同学帮助我们创建一个干净的python虚拟环境
#
# pip install virtualenv
#然后要做的工作当然就是创建一个虚拟环境啦
# virtualenv example_env  # 命名请随意
# 创建完成以后我们就会在python的Script文件夹里发现一个 与刚刚命名相同的文件夹
# 用cmd cd 到虚拟环境的Script目录然后 输入active回车
# 就可以开始愉快地pip安装必要模块 然后pyinstaller啦
