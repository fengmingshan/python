# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:22:07 2020

@author: Administrator
"""

from flask import Flask, url_for, request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
import os
import pandas as pd


app = Flask(__name__)


engine_mr = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/mr_report?charset=utf8", pool_recycle=7200)
engine_cqi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/cqi_report?charset=utf8", pool_recycle=7200)
engine_tousu = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/qjwx_tousu?charset=utf8",
                             pool_recycle=7200)
engine_kpi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/kpi_report?charset=utf8", pool_recycle=7200)
engine_rrc = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/rrc_reconnect?charset=utf8",
                           pool_recycle=7200)
engine_handover = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/hand_over?charset=utf8",
                           pool_recycle=7200)

Session_mr = sessionmaker(autocommit=False, autoflush=True, bind=engine_mr)
Session_cqi = sessionmaker(autocommit=False, autoflush=True, bind=engine_cqi)
Session_tousu = sessionmaker(autocommit=False, autoflush=True, bind=engine_tousu)
Session_kpi = sessionmaker(autocommit=False, autoflush=True, bind=engine_kpi)
Session_rrc = sessionmaker(autocommit=False, autoflush=True, bind=engine_rrc)
Session_handover = sessionmaker(autocommit=False, autoflush=True, bind=engine_handover)

session_mr = Session_mr()
session_cqi = Session_cqi()
session_tousu = Session_tousu()
session_kpi = Session_kpi()
session_rrc = Session_rrc()
session_handover = Session_handover()


cur_week = 24
# 从 rrc_reconnect 库提取 rrc重建比例top小区
rrc_roncon_top = session_rrc.execute(
    "INSERT INTO  `rrc重建比例TOP小区` SELECT `站号`, `小区号`,`小区名称`, `周` ,`RRC重建立比例`, `RRC重建请求数目`, `RRC连接重建成功率`,`切换失败触发的RRC重建立请求次数`, `其它原因触发的RRC重建立请求次数`, `重配失败触发的RRC重建立请求次数` FROM `rrc重建` WHERE `RRC重建立比例`> 0.1 and `周`= {week} ORDER BY `RRC重建请求数目` DESC LIMIT 50".format(week = cur_week)
)

# 将 rrc重建比例top小区 入库到 hande_over库
session_rrc.commit()
session_rrc.close()



