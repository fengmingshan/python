from flask import Flask, render_template, url_for
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
from pyecharts.faker import Faker
import os
import pandas

work_path = 'd:/_python小程序/话务报表WEB_APP/'
os.chdir(work_path)

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('report_index.html')

@app.route('/week')
def week_report():
    return render_template('week_report.html')

if __name__ == '__main__':
    app.run()
