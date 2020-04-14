from flask import Flask, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库参数
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.44:3306/mr_report?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

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
    context = {
        'username':'xxx',
        'age':18,
        'height':180,
    }
    return render_template('index.html',context=context,u_name = u_name)

# 传入一个数字显示一个range
@app.route('/ran/<int:num_range>')
def ran(num_range):
    n_range = range(num_range)
    context = {
        'username':'xxx',
        'age':18,
        'height':180,
    }
    return render_template('index.html',context=context,u_name = 'admin',n_range = n_range)

# 传入一个数值查数据库
@app.route('/query/<int:date_num>')
def queryu(date_num):
    query_date_num = date_num
    report = db.session.execute("select area,mr_good_rate from mr_summary where day(date_time) = {} and static_zone = '全市';".format(query_date_num))
    report =list(report)
    return render_template('query.html',report=report,query_date_num = query_date_num)

if __name__ == '__main__':
    app.run()