# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:39:19 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
import numpy as np
import csv
import os

# 配置数据库参数
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.44:3306/mr_report?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# =============================================================================
# 数据入库
# =============================================================================
# 建立Mr_summary数据库类，用来映射到数据库中的mr_summary表
class Mr_summary(db.Model):
    # 声明表名
    __tablename__ = 'mr_summary'
    # 建立字段函数
    primary_key = db.Column(db.String(255), primary_key=True)
    area = db.Column(db.String(255))
    date = db.Column(db.Date)
    cell_num = db.Column(db.Integer)
    is_800 = db.Column(db.String(10))
    above105 = db.Column(db.Float)
    between110and105 = db.Column(db.Float)
    between115and110 = db.Column(db.Float)
    between120and115 = db.Column(db.Float)
    inf = db.Column(db.Float)
    mr_good_rate = db.Column(db.Float)

    def __repr__(self):
        return '<User area: {}, date: {}, is_800: {}, mr_good_rate: {}>'.format(
            self.area, self.date, self.is_800, self.mr_good_rate)

# 建立Mr_summary数据库类，用来映射到数据库中的mr_summary表
class Mr_detail(db.Model):
    # 声明表名
    __tablename__ = 'mr_detail'
    # 建立字段函数
    primary_key = db.Column(db.String(255), primary_key=True)
    area = db.Column(db.String(255))
    date = db.Column(db.Date)
    NAME = db.Column(db.String(255))
    factory = db.Column(db.String(20))
    is_800 = db.Column(db.String(10))
    avg_rsrp = db.Column(db.Float)
    above105 = db.Column(db.Integer)
    between110and105 = db.Column(db.Integer)
    between115and110 = db.Column(db.Integer)
    between120and115 = db.Column(db.Integer)
    inf = db.Column(db.Integer)
    total = db.Column(db.Integer)
    mr_good = db.Column(db.Integer)
    mr_good_rate = db.Column(db.Float)

    def __repr__(self):
        return '<User area: {}, date: {}, is_800: {}, avg_rsrp: {}, total: {}, mr_good: {}, mr_good_rate: {}>'.format(
            self.area, self.date, self.is_800, self.avg_rsrp, self.total, self.mr_good, self.mr_good_rate)
db.create_all()

pro_y_name1 = Mr_summary.query.with_entities(Mr_summary.area).distinct().all()
pro_y_name1 = [x[0] for x in pro_y_name1]

pro_y_name2 = db.session.execute('select distinct area from mr_summary')
pro_y_name2 = [x[0] for x in pro_y_name2]

pro_y_data1 = db.session.query(Mr_summary.area, func.avg(Mr_summary.mr_good_rate)).group_by(Mr_summary.area)
pro_y_data1 = list(pro_y_data1)
pro_y_name1 = [x[0] for x in pro_y_data1]
pro_y_value1 = [x[1] for x in pro_y_data1]


pro_y_data2 = db.session.execute('select distinct area,round(avg(mr_good_rate),4) from mr_summary group by area')
pro_y_data2 = list(pro_y_data2)
pro_y_name2 = [x[0] for x in pro_y_data2]
pro_y_value2 = [x[1] for x in pro_y_data2]
