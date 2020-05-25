from flask import Flask, url_for
from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 配置数据库参数
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.44:3306/mr_report?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


def draw_line(x_axis,y_name1,y_data1):
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
                title_opts=opts.TitleOpts(title=title),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            )
    )
    return c

# 传入一个数值查数据库并绘图
@app.route('/chart/<int:date_num>')
def chart(date_num):
    report = db.session.execute("select area,mr_good_rate from mr_summary where day(date_time) = {} and static_zone = '全市';".format(date_num))
    report =list(report)
    x_axis = [x[0] for x in report]
    y_data = [round(x[1]*100,2) for x in report]
    chart1 = draw_bar(x_axis,'全省MR优良率',y_data,'全省各州市MR优良率')
    return render_template('show_top_cell.html',chart1_options=chart1.dump_options())

@app.route('/')
def hello_world():
    return render_template('kpi_index.html')


if __name__ == '__main__':
    app.run()
