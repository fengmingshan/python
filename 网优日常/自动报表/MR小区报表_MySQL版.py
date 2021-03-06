# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:37:59 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
import numpy as np
import os

work_path = 'D:\_python小程序\MR报表'
os.chdir(work_path)
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
class Mr_detail(db.Model):
    # 声明表名
    __tablename__ = 'mr_detail'
    # 建立字段函数
    primary_key = db.Column(db.String(255), primary_key=True)
    area = db.Column(db.String(255))
    date = db.Column(db.Date)
    NAME = db.Column(db.String(255))
    factory = db.Column(db.String(20))
    static_zone = db.Column(db.String(10))
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
            self.area, self.date, self.static_zone, self.avg_rsrp, self.total, self.mr_good, self.mr_good_rate)
db.create_all()

mr_data = db.session.execute(
    "select NAME,round(sum(mr_good)/sum(total),4)*100 from mr_detail where factory = '中兴' group by NAME order by round(sum(mr_good)/sum(total),4)*100 asc")
mr_data = list(mr_data)
cell_name = [x[0] for x in mr_data]
avg_good_rate = [float(x[1]) for x in mr_data]
df_mr_top = pd.DataFrame({'cell_name':cell_name,'avg_good_rate':avg_good_rate})
with pd.ExcelWriter('MR小区指标.xlsx') as f:
    df_mr_top.to_excel(f,'MR小区指标',index =False)