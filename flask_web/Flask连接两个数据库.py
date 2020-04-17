from flask import Flask, url_for
from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyecharts.faker import Faker

app = Flask(__name__)
engine_mr = create_engine("mysql+pymysql://root:a123456@218.63.75.44:3306/mr_report?charset=utf8")
engine_cqi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/cqi_report?charset=utf8")

# 配置数据库参数
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
SQLALCHEMY_BINDS = SQLALCHEMY_BINDS

Session1 = sessionmaker(autocommit=False, autoflush=False, bind=engine_mr)
Session2 = sessionmaker(autocommit=False, autoflush=False, bind=engine_cqi)
session1 = Session1()
session2 = Session2()

pro_data = session1.execute(
    "select area,round(sum(mr_good)/sum(total),4)*100 from mr_summary where static_zone = '全市' group by area order by round(sum(mr_good)/sum(total),4)*100 desc")
pro_data = list(pro_data)
pro_x_axis = [x[0] for x in pro_data]
pro_y_data = [float(x[1]) for x in pro_data]


pro_data_not800 = session2.execute("select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '爱立信800M' order by date_time asc;")
pro_data_not800 = list(pro_data_not800)
pro_x_axis_not800 = [x[0] for x in pro_data_not800]
pro_y_data_not800 = [x[1] for x in pro_data_not800]