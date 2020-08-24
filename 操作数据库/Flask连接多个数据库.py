# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:49:29 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/test?charset=utf8"
DB_URI_binds1 = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(username='root',
                                                                            password='a123456',
                                                                            host='localhost',
                                                                            port=3306,
                                                                            database='test1')
DB_URI_binds2 = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(username='root',
                                                                            password='a123456',
                                                                            host='localhost',
                                                                            port=3306,
                                                                            database='test2')
SQLAlchemy_binds_local = {
    "test1": DB_URI_binds1,
    "test2": DB_URI_binds2,
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_BINDS'] = SQLAlchemy_binds_local
#建立数据库对象

db = SQLAlchemy(app)


class User(db.Model):
    # 声明表名
    __tablename__ = 'user'
    # 建立字段函数
    no = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), primary_key=True)
    passwd = db.Column(db.String(255))

    def __repr__(self):
        return '<User ID: {}  用户名：{} 密码：{}>'.format(self.id, self.name, self.password)

db.create_all()
user = User(no = 2,name = 'admin',passwd ='root') # 自动关联到相对应的ORM模型,进而使用相关联的数据库引擎
user3 = User(no = 3,name = 'test',passwd ='a123') # 自动关联到相对应的ORM模型,进而使用相关联的数据库引擎

db.session.add(user) # 插入一条数据
db.session.add(user3) # 插入一条数据
db.session.commit()

li = User.query.order_by('no').limit(1)
li_name  = [x.name for x in li]
li_passwd  = [x.passwd for x in li]

li1 = db.session.execute('SELECT * FROM user')
li1_name  = [x.name for x in li1]

class User1(db.Model):
    #声明表名
    __tablename__ = 'user1'
    __bind_key__ = 'test1'
    #建立字段函数
    no = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __repr__(self):
        return '<User ID: {}  用户名：{} 密码：{}>'.format(self.id, self.name, self.password)

db.create_all(bind='test1')
user4 = User1(no = 4,name = 'root1',password ='passwd') # 自动关联到相对应的ORM模型,进而使用相关联的数据库引擎
user5 = User1(no = 5,name = 'root2',password ='a123456') # 自动关联到相对应的ORM模型,进而使用相关联的数据库引擎
user6 = User1(no = 6,name = 'root3',password ='a123') # 自动关联到相对应的ORM模型,进而使用相关联的数据库引擎

db.session.add(user4) # 插入一条数据
db.session.add(user5) # 插入一条数据
db.session.commit()

li1 = User1.query.order_by('no')
li1_name  = [x.name for x in li1]
li1_passwd  = [x.password for x in li1]

li2 = db.session.execute('SELECT * FROM user1', bind=db.get_engine(app,bind='test1'))
li2_name  = [x.name for x in li2]
