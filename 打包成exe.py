pyinstaller -F *.py

#含有pandas库的容易报错，需要加以下参数
pyinstaller --clean --win-private-assemblies -F MR.py  
pyinstaller --clean --win-private-assemblies -F MR-win.py  


pyinstaller --clean --win-private-assemblies -F CQI_LC.py 

hiddenimports = ['pandas._libs.tslibs.timedeltas',
'pandas._libs.tslibs.nattype',
'pandas._libs.tslibs.np_datetime',
'pandas._libs.skiplist']
cd D:\test\

pyinstaller -F MR.py