# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:09:14 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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


work_path = 'D:/_python小程序/MR报表'
os.chdir(work_path)
all_files = os.listdir('./原始数据')
summary_files = [x for x in all_files if '总表' in x]
detail_files = [x for x in all_files if '详表' in x]

# 处理总表
summary_list = []
for file in summary_files:
    df_tmp = pd.read_csv('./原始数据/' + file, sep=',', engine='python')
    summary_list.append(df_tmp)
df_summary = pd.concat(summary_list, axis=0)
df_summary.reset_index(drop=True, inplace=True)
df_summary.rename(columns={'区域': 'area',
                           '时间周期': 'date',
                           '扇区数量': 'cell_num',
                           '是否800M设备': 'is_800',
                           '|≥-105dBm比例': 'above105',
                           '|-110<=RSRP<-105dBm比例': 'between110and105',
                           '|-115<=RSRP<-110dBm比例': 'between115and110',
                           '|-120<=RSRP<-115dBm比例': 'between120and115',
                           '|≥负无穷比例': 'inf'
                           }, inplace=True)
df_summary['date'] = pd.to_datetime(df_summary['date'])
df_summary['date'] = df_summary['date'].map(lambda x: str(x).split(' ')[0])
for col in ['above105', 'between110and105', 'between115and110', 'between120and115', 'inf']:
    df_summary[col] = df_summary[col].astype(float)
df_summary['mr_good_rate'] = round((df_summary['above105'] + df_summary['between110and105']),3)
df_summary['primary_key'] = df_summary['area'] + '_' + df_summary['is_800'] + '_' + df_summary['date']
df_summary = df_summary[['primary_key', 'area', 'date', 'cell_num', 'is_800', 'above105', 'between110and105',
       'between115and110', 'between120and115', 'inf', 'mr_good_rate']]

# 处理详表
col = [
    '区域',
    '时间周期',
    'NAME',
    '厂家',
    '是否800M设备',
    '平均RSRP（dBm）',
    '|≥-105dBm采样点',
    '|≥-110dBm采样点',
    '|≥-115dBm采样点',
    '|≥-120dBm采样点',
    '|≥负无穷采样点']
detail_list = []
for file in detail_files:
    with open('./原始数据/' + file, 'r', newline='')as f:
        reader = csv.reader(f, delimiter=',')
        rows = [x[0:2] + [','.join(x[2:-8])] + x[-8:] for x in reader]
        df_tmp = pd.DataFrame(rows[1:], columns=col)
        df_tmp = df_tmp[df_tmp['区域'] == '曲靖市']
        detail_list.append(df_tmp)
df_detail = pd.concat(detail_list, axis=0)
df_detail.reset_index(drop=True, inplace=True)
df_detail.rename(columns={'区域': 'area',
                          '时间周期': 'date',
                          '厂家': 'factory',
                          '是否800M设备': 'is_800',
                          '平均RSRP（dBm）': 'avg_rsrp',
                          '|≥-105dBm采样点': 'above105',
                          '|≥-110dBm采样点': 'between110and105',
                          '|≥-115dBm采样点': 'between115and110',
                          '|≥-120dBm采样点': 'between120and115',
                          '|≥负无穷采样点': 'inf'
                          }, inplace=True)
df_detail['date'] = pd.to_datetime(df_detail['date'])
df_detail['date'] = df_detail['date'].map(lambda x: str(x).split(' ')[0])
df_detail['avg_rsrp'] = df_detail['avg_rsrp'].astype(float)
for col in ['above105', 'between110and105', 'between115and110', 'between120and115', 'inf']:
    df_detail[col] = df_detail[col].astype(int)
df_detail['total'] = df_detail['above105'] + df_detail['between110and105']+ df_detail['between115and110']+ df_detail['between120and115']+ df_detail['inf']
df_detail['mr_good'] = df_detail['above105'] + df_detail['between110and105']
df_detail['mr_good_rate'] = round(df_detail['mr_good']/df_detail['total'],3)
df_detail['primary_key'] = df_detail['NAME'] + '_' + df_detail['date']
df_detail = df_detail[['primary_key', 'area', 'date', 'NAME', 'factory', 'is_800', 'avg_rsrp', 'above105',
       'between110and105', 'between115and110', 'between120and115', 'inf', 'total', 'mr_good', 'mr_good_rate']]

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
db.create_all()

# 入库 df_summary 数据
# 校验主键是否重复
# db.session.rollback()
key_list = Mr_summary.query.with_entities(Mr_summary.primary_key).distinct().all()
key_list = [x[0] for x in key_list]
df_summary = df_summary[~df_summary['primary_key'].isin(key_list)]
summary_data = [Mr_summary(
    primary_key=primary_key,
    area=area,
    date=date,
    cell_num=cell_num,
    is_800=is_800,
    above105=above105,
    between110and105=between110and105,
    between115and110=between115and110,
    between120and115=between120and115,
    inf=inf,
    mr_good_rate=mr_good_rate
)
    for primary_key,area, date, cell_num, is_800, above105, between110and105, between115and110, between120and115, inf, mr_good_rate
    in zip(
        df_summary['primary_key'],
        df_summary['area'],
        df_summary['date'],
        df_summary['cell_num'],
        df_summary['is_800'],
        df_summary['above105'],
        df_summary['between110and105'],
        df_summary['between115and110'],
        df_summary['between120and115'],
        df_summary['inf'],
        df_summary['mr_good_rate'],
    )
]
for item in summary_data:
    db.session.add(item)
db.session.commit()

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

# 入库 df_detail 数据
# 校验主键是否重复
# db.session.rollback()
key_list = Mr_summary.query.with_entities(Mr_detail.primary_key).distinct().all()
key_list = [x[0] for x in key_list]
df_detail = df_detail[~df_detail['primary_key'].isin(key_list)]

detail_data = [Mr_detail(
    primary_key=primary_key,
    area=area,
    date=date,
    NAME=NAME,
    factory=factory,
    is_800=is_800,
    avg_rsrp=avg_rsrp,
    above105=above105,
    between110and105=between110and105,
    between115and110=between115and110,
    between120and115=between120and115,
    inf=inf,
    total=total,
    mr_good=mr_good,
    mr_good_rate=mr_good_rate
)
    for primary_key,area, date, NAME, factory, is_800, avg_rsrp, above105, between110and105, between115and110, between120and115, inf, total, mr_good, mr_good_rate
    in zip(
        df_detail['primary_key'],
        df_detail['area'],
        df_detail['date'],
        df_detail['NAME'],
        df_detail['factory'],
        df_detail['is_800'],
        df_detail['avg_rsrp'],
        df_detail['above105'],
        df_detail['between110and105'],
        df_detail['between115and110'],
        df_detail['between120and115'],
        df_detail['inf'],
        df_detail['total'],
        df_detail['mr_good'],
        df_detail['mr_good_rate'],
    )
]

for item in detail_data:
    db.session.add(item)
db.session.commit()
