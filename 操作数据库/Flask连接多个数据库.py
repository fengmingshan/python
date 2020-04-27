# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:49:29 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import create_engine
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/test123?charset=utf8"
DB_URI_binds = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(username='root',
                                                                            password='a123456',
                                                                            host='218.63.75.43',
                                                                            port=3306,
                                                                            database='mr_report')
DB_URI_binds2 = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(username='root',
                                                                            password='a123456',
                                                                            host='localhost',
                                                                            port=3306,
                                                                            database='test123')

SQLAlchemy_binds_local = {
    "mr_report": DB_URI_binds,
    "test123": DB_URI_binds2

}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_BINDS'] = SQLAlchemy_binds_local
#建立数据库对象
db = SQLAlchemy(app)


class Mr_summary(db.Model):
    # 声明表名
    __bind_key__ = 'mr_report'
    __tablename__ = 'mr_summary'
    # 建立字段函数
    primary_key = db.Column(db.String(255), primary_key=True)
    area = db.Column(db.String(255))
    date_time = db.Column(db.Date)
    static_zone = db.Column(db.String(10))
    above105 = db.Column(db.Integer)
    between110and105 = db.Column(db.Integer)
    between115and110 = db.Column(db.Integer)
    between120and115 = db.Column(db.Integer)
    inf = db.Column(db.Integer)
    total = db.Column(db.Integer)
    mr_good = db.Column(db.Integer)
    mr_good_rate = db.Column(db.Float)

    def __repr__(self):
        return '<User area: {}, date: {}, static_zone: {}, mr_good_rate: {}>'.format(
            self.area, self.date_time, self.static_zone, self.mr_good_rate)
db.create_all(bind='mr_report')
li = Mr_summary.query.filter_by(area='曲靖市').all()
li_area  = [x.area for x in li]
li_mr_good_rate  = [x.mr_good_rate for x in li]

class User(db.Model):
    #声明表名
    __tablename__ = 'user'
    __bind_key__ = 'test123'
    #建立字段函数
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    def __repr__(self):
        return '<User ID: {}  用户名：{} 密码：{}>'.format(self.id, self.name, self.password)
db.create_all(bind='test123')
li1 = User.query.order_by('id').all()
li1_name  = [x.name for x in li1]
li1_password  = [x.password for x in li1]

