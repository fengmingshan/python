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
path = r'C:\Users\Administrator\Desktop'
os.chdir(path)

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip


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


def draw_line(x_axis,y_name1,y_data1,title):
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
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axislabel_opts=opts.LabelOpts(rotate=-30),
                ),
                yaxis_opts=opts.AxisOpts(
                    name=y_name1,
                    type_="value",
                ),
                title_opts=opts.TitleOpts(
                    title=title,
                    title_textstyle_opts=opts.TextStyleOpts(
                        color="#6a98ab"
                    )
                ),
            )
            .reversal_axis()
    ).render("./line_reversal_axis.html")

def draw_bar(x_axis,y_name,y_data,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name, y_data)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                pos_top='top',
            ),
        )
    ).render("./bar_reversal_axis.html")

def draw_bar_stack(x_axis,y_name1,y_data1,y_name2,y_data2,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1, y_data1, stack="stack1")
        .add_yaxis(y_name2, y_data2, stack="stack1")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-堆叠数据（全部）"))
    ).render("bar_stack.html")

recon_cnt = session_handover.execute(
        "SELECT `邻区`,`切换出成功次数`, `切换出失败次数`, `切换出成功率`, `切换入成功次数`, `切换入失败次数`, `切换入成功率` FROM `邻区切换` WHERE eNodeB = 731611 and `小区` = 18 and (`切换出请求总次数`>30 OR `切换入请求总次数`>30) order by `切换出请求总次数` asc")
recon_cnt = list(recon_cnt)
neibor = [x.邻区 for x in recon_cnt]
handout_succ_cnt = [x.切换出成功次数 for x in recon_cnt]
handout_faied_cnt = [x.切换出失败次数 for x in recon_cnt]
handout_succ_ratio = [float(x.切换出成功率.replace('%','')) for x in recon_cnt]
handin_succ_cnt = [x.切换入成功次数 for x in recon_cnt]
handin_faied_cnt = [x.切换入失败次数 for x in recon_cnt]
handin_succ_ratio = [float(x.切换入成功率.replace('%','')) for x in recon_cnt]

rev_line = draw_line(neibor,'切换出成功率',handout_succ_ratio,'切换出成功率')
rev_bar = draw_bar(neibor, '切换出成功率', handout_succ_ratio, '切换出成功率')
bar_stack = draw_bar_stack(neibor, '切换出成功次数', handout_succ_cnt, '切换出失败次数', handout_faied_cnt,  '切换出次数')
#hand_succ = draw_bar_stack(neibor, '切换出成功率', handout_succ_ratio, '切换入成功率', handin_succ_ratio,  '切换成功率')

