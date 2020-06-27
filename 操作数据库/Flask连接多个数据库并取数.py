# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:00:39 2020

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


path = r'C:\Users\Administrator\Desktop'
os.chdir(path)

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


def draw_line2(title,x_axis,y_name1,y_data1,y_name2,y_data2):
    c = (
        Line()
            .add_xaxis(xaxis_data=x_axis)
            .add_yaxis(
            series_name=y_name1,
            y_axis=y_data1,
            symbol="circle",
            symbol_size=10,
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=True),
            linestyle_opts=opts.LineStyleOpts(width=3)
            )
            .add_yaxis(
            series_name=y_name2,
            y_axis=y_data2,
            symbol="circle",
            symbol_size=10,
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=True),
            linestyle_opts=opts.LineStyleOpts(width=3)
            )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(rotate=-30),
                ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            title_opts=opts.TitleOpts(title=title),
            )
    )
    return c


def draw_bar(y_name1,y_data1,x_axis,title):
    c = (
        Bar()
            .add_xaxis(x_axis)
            .add_yaxis(y_name1, y_data1,category_gap="60%")
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title,title_textstyle_opts=opts.TextStyleOpts(color="#6a98ab")),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
                yaxis_opts=opts.AxisOpts(
                    name= y_name1,
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
    )
    return c



recon_ratio = session_rrc.execute(
    "SELECT * from `rrc重建比例top小区` where 站号 = {enb} and `小区号` ={cell} LIMIT 5".format(
        enb=enb, cell=cell))
recon_ratio = list(recon_ratio)
cell_name = recon_ratio[0].小区名称
ratio = [x.RRC重建立比例 for x in recon_ratio]
ratio_sec = [x.RRC连接重建成功率 for x in recon_ratio]
recon_count = [x.RRC重建请求数目 for x in recon_ratio]
recon_ratio_chart = draw_line2(' ', weeks, 'RRC重建比例', ratio, 'RRC连接重建成功率', ratio_sec)
recon_count_chart = draw_bar('RRC重建请求次数', recon_count, weeks, 'RRC重建次数', )

recon_reason = recon_ratio[0][6:]
recon_reason_chart = draw_pie(['切换失败', '其它原因', '重配失败'], recon_reason, 'RRC重建原因:', 'RRC重建原因')
