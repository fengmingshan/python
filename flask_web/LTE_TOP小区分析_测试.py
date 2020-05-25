# -*- coding: utf-8 -*-
"""
Created on Fri May 15 10:18:50 2020

@author: Administrator
"""

from flask import Flask, url_for, request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
engine_kpi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/kpi_report?charset=utf8",pool_recycle = 7200)

Session4 = sessionmaker(autocommit=False, autoflush=True, bind=engine_kpi)

session4 = Session4()

cur_week = session4.execute("SELECT max(week(zte_day_5.`开始时间`)) from zte_day_5")
cur_week = list(cur_week)[0][0]
top_cells = session4.execute("SELECT zte_day_5.`网元`,zte_day_5.`小区` FROM zte_day_5 where week(zte_day_5.`开始时间`) = {week} order by zte_day_5.`RRC连接重建比例_1` DESC LIMIT 20".format(week = cur_week))
top_cells = list(top_cells)
top_cells_enb = [x.网元 for x in top_cells]
top_cells_cell = [x.小区 for x in top_cells]
top_cells_info = [str(x)+"_"+str(y) for x,y in zip(top_cells_enb,top_cells_cell)]

