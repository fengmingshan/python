# 切换到服务器端中文路径报错
folder = '/MR报表/日报表'
cwd(folder.encode('utf-8').decode('latin1'))

# 下载中文名文件报错,修改 ftplib.FTP 类的类属性

from ftplib import FTP
ftp = FTP()
ftp.encoding = 'utf-8'

