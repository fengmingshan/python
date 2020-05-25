# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:16:45 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

work_path = 'd:/_python/python/操作数据库/'
os.chdir(work_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/eric_traffic?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True

# 建立数据库对象
db = SQLAlchemy(app)
#db = SQLAlchemy(app, use_native_unicode='utf8')

title = ['key',
         'week',
         'eNodeB',
         'EUTRANCELLFDD',
         'Acc_WirelessConnSucRate',
         'Acc_ERAB_droppingrate',
         'AirInterface_Traffic_Volume_UL_MBytes',
         'AirInterface_Traffic_Volume_DL_MBytes',
         'Int_DownlinkLatency',
         'MaxnumberofUEinRRc',
         'pmCellDowntimeAuto1',
         'pmCellDowntimeMan1',
         'Data_Coverage',
         'Ava_CellAvail',
         'NumofLTERedirectto3G',
         'AvgNumberofULActiveUsers',
         'AvgNumberofDLActiveUsers',
         'DL_Util_of_PRB',
         'DLactiveuesum',
         'CellPDCPDLbit',
         'AvgUserFellThroughput_Mbps'
         ]

df_eric = pd.read_csv('./爱立信0224-0301_mini.csv', header=None, names=title)
df_eric = df_eric[['key',
                   'week',
                   'eNodeB',
                   'EUTRANCELLFDD',
                   'Acc_WirelessConnSucRate',
                   'Acc_ERAB_droppingrate',
                   'AirInterface_Traffic_Volume_UL_MBytes',
                   'AirInterface_Traffic_Volume_DL_MBytes',
                   'Int_DownlinkLatency',
                   'MaxnumberofUEinRRc',
                   'AvgNumberofULActiveUsers',
                   'AvgNumberofDLActiveUsers',
                   'DL_Util_of_PRB',
                   'AvgUserFellThroughput_Mbps'
                   ]]

# 建立数据库类，用来映射到数据库中的表。
class Eric_day(db.Model):
    # 声明表名
    __tablename__ = 'eric_day'
    # 建立字段函数
    key = db.Column(db.String(200), primary_key=True)
    week = db.Column(db.Integer)
    eNodeB = db.Column(db.String(200))
    EUTRANCELLFDD = db.Column(db.String(200))
    Acc_WirelessConnSucRate = db.Column(db.Float)
    Acc_ERAB_droppingrate = db.Column(db.Float)
    AirInterface_Traffic_Volume_UL_MBytes = db.Column(db.Float)
    AirInterface_Traffic_Volume_DL_MBytes = db.Column(db.Float)
    Int_DownlinkLatency = db.Column(db.Float)
    MaxnumberofUEinRRc = db.Column(db.Integer)
    AvgNumberofULActiveUsers = db.Column(db.Float)
    AvgNumberofDLActiveUsers = db.Column(db.Float)
    DL_Util_of_PRB = db.Column(db.Float)
    AvgUserFellThroughput_Mbps = db.Column(db.Float)

    def __repr__(self):
        return '<User key: {}, week: {}, eNodeB: {}, EUTRANCELLFDD: {}, Acc_WirelessConnSucRate: {}, Acc_ERAB_droppingrate: {}>'.format(
            self.key, self.week, self.eNodeB, self.EUTRANCELLFDD, self.Acc_WirelessConnSucRate, self.Acc_ERAB_droppingrate)


#db.drop_all()
db.create_all()

# =============================================================================
# 导入数据
# =============================================================================
traffic_data = [Eric_day(
    key=key,
    week=wk,
    eNodeB=enb,
    EUTRANCELLFDD=cell,
    Acc_WirelessConnSucRate=accrate,
    Acc_ERAB_droppingrate=drop,
    AirInterface_Traffic_Volume_UL_MBytes=uth,
    AirInterface_Traffic_Volume_DL_MBytes=dth,
    Int_DownlinkLatency=lat,
    MaxnumberofUEinRRc=mrrc,
    AvgNumberofULActiveUsers=uact,
    AvgNumberofDLActiveUsers=dact,
    DL_Util_of_PRB=prb,
    AvgUserFellThroughput_Mbps=fell
) for key,wk, enb, cell, accrate, drop, uth, dth, lat, mrrc, uact, dact, prb, fell in zip(
    df_eric['key'],
    df_eric['week'],
    df_eric['eNodeB'],
    df_eric['EUTRANCELLFDD'],
    df_eric['Acc_WirelessConnSucRate'],
    df_eric['Acc_ERAB_droppingrate'],
    df_eric['AirInterface_Traffic_Volume_UL_MBytes'],
    df_eric['AirInterface_Traffic_Volume_DL_MBytes'],
    df_eric['Int_DownlinkLatency'],
    df_eric['MaxnumberofUEinRRc'],
    df_eric['AvgNumberofULActiveUsers'],
    df_eric['AvgNumberofDLActiveUsers'],
    df_eric['DL_Util_of_PRB'],
    df_eric['AvgUserFellThroughput_Mbps']
)]

for item in traffic_data:
    db.session.add(item)
db.session.commit()

# 原生SQL语句方式
#db.session.execute(r'insert into user values (8, "wjz", "test123")')
#db.session.execute(r'insert into user values (9, "wjz", "admin123")')
#
#db.session.commit()


# =============================================================================
# 查表
# =============================================================================

# ORM方式
btslist = Eric_day.query.order_by('eNodeB').all()
# 使用class User定义好的格式进行print
for bts in btslist:
    print(bts)

# 自定义格式print
for bts in btslist:
    print(bts.week, ' ', bts.eNodeB, ' ', bts.EUTRANCELLFDD, ' ', bts.Acc_WirelessConnSucRate, ' ', bts.Acc_ERAB_droppingrate)


# 原生数据库语句_推荐
item = db.session.execute('select * from user order by id asc')
# #将结果集强转为list
item = list(item)
for i in item:
    print(i)


# =============================================================================
# 删除内容
# =============================================================================
# ORM方式
# User.query.filter_by(id=6).delete()
# User.query.filter_by(id=7).delete()
# User.query.filter_by(id=8).delete()
# User.query.filter_by(id=9).delete()
# db.session.commit()
#
# 原生SQL语句方式
#db.session.execute(r'delete from user where id = 7')
# db.session.commit()

# =============================================================================
# 修改内容
# =============================================================================
# ORM方式
# User.query.filter_by(id=3).update({'name':'张三'})
# User.query.filter_by(id=4).update({'name':'李四'})
# db.session.commit()
#
# 原生SQL语句方式
#db.session.execute(r'update user set name="李四" where id= 4')
#db.session.execute(r'update user set name="王二" where id= 5')
# db.session.commit()
#
#userlist1 = User.query.order_by('id').all()
