# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:13:40 2020

@author: Administrator
"""
import pandas as pd
import os
from pandas import Series,DataFrame
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

path =r'C:\Users\Administrator\Desktop\栅格'
os.chdir(path)
files = os.listdir(path)

# =============================================================================
# 通过生成器读取大型 excel 文件
# =============================================================================
def read_csv_partly(file):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=50000)
    for df_tmp in file_data:
        yield df_tmp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/rsrp_grid50?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True

# 建立数据库对象
db = SQLAlchemy(app)
class rsrp_grid50(db.Model):
    # 声明表名
    __tablename__ = 'rsrp_grid_09'
    # 建立字段函数
    key=db.Column(db.String(200),primary_key=True)
    SDATE=db.Column(db.DateTime)
    CITY=db.Column(db.String(200))
    SC_ECI=db.Column(db.BIGINT)
    GRIDX=db.Column(db.BIGINT)
    GRIDY=db.Column(db.BIGINT)
    NUM_HOURS=db.Column(db.Integer)
    AVG_SCRSRP=db.Column(db.Float)
    RSRP_SAMPLES=db.Column(db.BIGINT)
    AVG_SCRSRQ=db.Column(db.Float)
    RSRQ_SAMPLES=db.Column(db.BIGINT)
    FREQ=db.Column(db.Integer)
    EARFCN=db.Column(db.Integer)
    CELLID=db.Column(db.Integer)
    eNB=db.Column(db.Integer)
    cell_ind=db.Column(db.String(200))
    def __repr__(self):
        return '<User key:{},SDATE:{},CITY:{},SC_ECI:{},GRIDX:{},GRIDY:{},NUM_HOURS:{},AVG_SCRSRP:{},RSRP_SAMPLES:{},AVG_SCRSRQ:{},RSRQ_SAMPLES:{},FREQ:{},EARFCN:{},CELLID:{},eNB:{},cell_ind:{}>'.format(
            self.key,self.SDATE,self.CITY,self.SC_ECI,self.GRIDX,self.GRIDY,self.NUM_HOURS,self.AVG_SCRSRP,self.RSRP_SAMPLES,self.AVG_SCRSRQ,self.RSRQ_SAMPLES,self.FREQ,self.EARFCN,self.CELLID,self.eNB,self.cell_ind)
db.create_all()

for file_name in files:
    list_df = []
    i = 1
    for df in read_csv_partly(file_name):
        list_df.append(df)
        df_rsrp = pd.concat(list_df,axis = 0)
        list_df.clear()
        
        df_rsrp["SDATE"] = df["SDATE"]
        df_rsrp["CITY"] = df["CITY"]
        df_rsrp["SC_ECI"] = df["SC_ECI"]
        df_rsrp["GRIDX"] = df["GRIDX"]
        df_rsrp["GRIDY"] = df["GRIDY"]
        df_rsrp["NUM_HOURS"] = df["NUM_HOURS"]
        df_rsrp["AVG_SCRSRP"] = df["AVG_SCRSRP"]
        df_rsrp["RSRP_SAMPLES"] = df["RSRP_SAMPLES"]
        df_rsrp["AVG_SCRSRQ"] = df["AVG_SCRSRQ"]
        df_rsrp["RSRQ_SAMPLES"] = df["RSRQ_SAMPLES"]
        df_rsrp["FREQ"] = df["FREQ"]
        df_rsrp["EARFCN"] = df["EARFCN"]
        df_rsrp["CELLID"] = df["CELLID"]
        df_rsrp["eNB"] = df["eNB"]
        df_rsrp["cell_ind"] = df["cell_ind"]
        df_rsrp['index1'] = df_rsrp.index
        df_rsrp["key"] = df_rsrp["SDATE"].map(str)+df_rsrp["cell_ind"].map(str)+df_rsrp["GRIDY"].map(str)+df_rsrp["AVG_SCRSRP"].map(str)+df_rsrp["AVG_SCRSRQ"].map(str)+df_rsrp["index1"].map(str)
        # =============================================================================
        # 导入数据
        # =============================================================================
        traffic_data = [rsrp_grid50(
            key=key,
            SDATE=st,
            CITY=et,
            SC_ECI=thg,
            GRIDX=sub,
            GRIDY=subn,
            NUM_HOURS=neb,
            AVG_SCRSRP=nen,
            RSRP_SAMPLES=cell,
            AVG_SCRSRQ=celln,
            RSRQ_SAMPLES=eno,
            FREQ=ucdr,
            EARFCN=aedr,
            CELLID=cuddst,
            eNB=cdddst,
            cell_ind=sssr
         )for key,st,et,thg,sub,subn,neb,nen,cell,celln,eno,ucdr,aedr,cuddst,cdddst,sssr in zip(
            df_rsrp['key'],
            df_rsrp['SDATE'],
            df_rsrp['CITY'],
            df_rsrp['SC_ECI'],
            df_rsrp['GRIDX'],
            df_rsrp['GRIDY'],
            df_rsrp['NUM_HOURS'],
            df_rsrp['AVG_SCRSRP'],
            df_rsrp['RSRP_SAMPLES'],
            df_rsrp['AVG_SCRSRQ'],
            df_rsrp['RSRQ_SAMPLES'],
            df_rsrp['FREQ'],
            df_rsrp['EARFCN'],
            df_rsrp['CELLID'],
            df_rsrp['eNB'],
            df_rsrp['cell_ind']
        )]
        
        for item in traffic_data:
            db.session.add(item)
        db.session.commit()            
        print('已入库: {}W条。'.format(i*5))
        i += 1
