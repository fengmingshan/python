from flask import Flask, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts
app = Flask(__name__)

# 配置数据库参数
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.44:3306/mr_report?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

def draw_bar(x_axis,y_name1,y_data1,title):
    c = (
        Bar()
            .add_xaxis(x_axis)
            .add_yaxis(y_name1, y_data1,category_gap="60%")
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            )
    )
    return c

# 主页默认显示：用户:admin的页面
@app.route('/')
def index():
    context = {
        'username':'xxx',
        'age':18,
        'height':180,
    }
    return render_template('index.html',context=context,u_name = 'admin')

# 传入用户名显示：用户:xxx的页面
@app.route('/user/<name>')
def name(name):
    u_name = name
    return render_template('user_index.html',u_name = u_name)

# 传入一个数字显示一个range
@app.route('/range/<int:num_range>')
def ran(num_range):
    n_range = range(num_range)
    return render_template('range.html',n_range = n_range)

# 传入一个数值查数据库
@app.route('/query/<int:date_num>')
def query(date_num):
    report = db.session.execute("select area,mr_good_rate from mr_summary where day(date_time) = {} and static_zone = '全市';".format(date_num))
    report =list(report)
    return render_template('query.html',report=report,query_date_num = date_num)

# 传入一个数值查数据库并绘图
@app.route('/chart/<int:date_num>')
def chart(date_num):
    report = db.session.execute("select area,mr_good_rate from mr_summary where day(date_time) = {} and static_zone = '全市';".format(date_num))
    report =list(report)
    x_axis = [x[0] for x in report]
    y_data = [round(x[1]*100,2) for x in report]
    chart1 = draw_bar(x_axis,'全省MR优良率',y_data,'全省各州市MR优良率')
    return render_template('chart.html',chart1_options=chart1.dump_options())

if __name__ == '__main__':
    app.run()