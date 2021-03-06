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


engine_mr = create_engine(
    "mysql+pymysql://root:a123456@218.63.75.43:3306/mr_report?charset=utf8", pool_recycle=7200)
engine_cqi = create_engine(
    "mysql+pymysql://root:a123456@218.63.75.43:3306/cqi_report?charset=utf8", pool_recycle=7200)
engine_tousu = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/qjwx_tousu?charset=utf8",
                             pool_recycle=7200)
engine_kpi = create_engine(
    "mysql+pymysql://root:a123456@218.63.75.43:3306/kpi_report?charset=utf8", pool_recycle=7200)
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


cur_week = 23
# 从 rrc_reconnect 库提取 rrc重建比例top小区
rrc_roncon_top = session_rrc.execute(
    "SELECT * from `rrc重建比例top小区` WHERE `周`= {week}".format(week=cur_week)
)
rrc_roncon_top = list(rrc_roncon_top)
week = tuple(x.周 for x in rrc_roncon_top)
enb = tuple(x.站号 for x in rrc_roncon_top)
cell = tuple(x.小区号 for x in rrc_roncon_top)
name = tuple(x.小区名称 for x in rrc_roncon_top)

# 将 rrc重建比例top小区 入库到 hande_over库
for wek, en, cel, nam in zip(week, enb, cell, name):
    session_handover.execute("INSERT INTO  `rrc重建top_index`(`周`, `站号`,  `小区号`, `小区名称`) VALUES ({wek},{enb},{cell},'{name}')".format(
        wek=wek, enb=en, cell=cel, name=nam))

session_handover.execute("update `rrc重建top_index` SET `cell_ind` = CONCAT(`站号`,'_',`小区号`)")

session_handover.execute(
    "INSERT INTO  `rrc重建比例TOP小区` SELECT `网元`,`小区`,concat(`网元`,'_',`小区`) ,`周`,`邻区`,`邻区关系`,`切换出请求总次数`,`切换出成功次数`, `切换出失败次数`, `切换出执行失败次数_源侧发生重建立`, `切换出执行失败次数_等待UECONTEXTRELEASE消息超时`, `切换出执行失败次数_其它原因`, `切换出准备失败次数_等待切换响应定时器超时`, `切换出准备失败次数_目标侧准备失败`, `切换出准备失败次数_其它原因`, `切换出准备失败次数_源侧发生重建立`, `切换出准备失败次数_用户未激活`, `切换出准备失败次数_传输资源受限`,`切换入成功次数`, `切换入失败次数`, `切换入执行失败次数_RRC重配完成超时`, `切换入执行失败次数_源侧取消切换`, `切换入执行失败次数_目标侧发生重建立`, `切换入执行失败次数_其他原因`, `切换入准备失败次数_资源分配失败`, `切换入准备失败次数_源侧取消切换`, `切换入准备失败次数_目标侧发生重建立`, `切换入准备失败次数_传输资源受限`, `切换入准备失败次数_其它原因` FROM `邻区切换` WHERE `周`= {week} and concat(`网元`,'_',`小区`) in (select `cell_ind` from `rrc重建top_index` WHERE `周`= {week});".format(week=cur_week))

session_handover.commit()
session_handover.close()
