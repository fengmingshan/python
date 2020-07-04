# 并行工作线程数
workers = 2

# 监听内网端口5000【按需要更改】
bind = '127.0.0.1:8002'

# 设置守护进程【关闭连接时，程序仍在运行】
daemon = True

# 设置超时时间120s，默认为30s。按自己的需求进行设置
timeout = 120

# 设置工作模式gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'gevent'

# 设置访问日志和错误信息日志路径
accesslog = './logs/acess.log'
errorlog = './logs/error.log'
