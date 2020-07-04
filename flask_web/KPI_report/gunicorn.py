# 并行工作线程数
workers = 4

# 监听内网端口5000【按需要更改】
bind = '127.0.0.1:8001'

# 设置守护进程【关闭连接时，程序仍在运行】
daemon = False

# 设置超时时间120s，默认为30s。按自己的需求进行设置
timeout = 60

# 设置工作模式gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'sync'

# 设置访问日志和错误信息日志路径
accesslog = '/home/fms/project/KPI_report/logs/gunicorn_acess.log'
errorlog = '/home/fms/project/KPI_report/logs/gunicorn_error.log'

 #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'info'

#设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s %(r)s %(s)s %(L)s %(b)s %(f)s %(a)s' 
