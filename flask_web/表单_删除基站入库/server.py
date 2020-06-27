from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer

from tornado.ioloop import IOLoop
import sys

# 将自定义包的路径添加在系统路径中
sys.path.insert(0, "E:/JupyterServer/del_bts2database")

from app import app
s = HTTPServer(WSGIContainer(app))
s.listen(8008) # 监听 8008 端口
IOLoop.current().start()