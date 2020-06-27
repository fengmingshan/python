from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer

from tornado.ioloop import IOLoop
import sys

# 将自定义包的路径添加在系统路径中
sys.path.insert(0, "D:/_python/python/flask_web/多个flask服务器")

from app3 import app
s = HTTPServer(WSGIContainer(app))
s.listen(8001) # 监听 8001 端口
IOLoop.current().start()