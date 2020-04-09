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

# 建立Mr_summary数据库类，用来映射到数据库中的mr_summary表
class Mr_summary(db.Model):
    # 声明表名
    __tablename__ = 'mr_summary'
    # 建立字段函数
    primary_key = db.Column(db.String(255), primary_key=True)
    area = db.Column(db.String(255))
    date_time = db.Column(db.Date)
    cell_num = db.Column(db.Integer)
    is_800 = db.Column(db.String(10))
    above105 = db.Column(db.Float)
    between110and105 = db.Column(db.Float)
    between115and110 = db.Column(db.Float)
    between120and115 = db.Column(db.Float)
    inf = db.Column(db.Float)
    mr_good_rate = db.Column(db.Float)

    def __repr__(self):
        return '<User area: {}, date: {}, is_800: {}, mr_good_rate: {}>'.format(
            self.area, self.date, self.is_800, self.mr_good_rate)

# 建立 Mr_detail 数据库类，用来映射到数据库中的 mr_detail 表
class Mr_detail(db.Model):
    # 声明表名
    __tablename__ = 'mr_detail'
    # 建立字段函数
    primary_key = db.Column(db.String(255), primary_key=True)
    area = db.Column(db.String(255))
    date_time = db.Column(db.Date)
    NAME = db.Column(db.String(255))
    factory = db.Column(db.String(20))
    is_800 = db.Column(db.String(10))
    avg_rsrp = db.Column(db.Float)
    above105 = db.Column(db.Integer)
    between110and105 = db.Column(db.Integer)
    between115and110 = db.Column(db.Integer)
    between120and115 = db.Column(db.Integer)
    inf = db.Column(db.Integer)
    total = db.Column(db.Integer)
    mr_good = db.Column(db.Integer)
    mr_good_rate = db.Column(db.Float)

    def __repr__(self):
        return '<User area: {}, date: {}, is_800: {}, avg_rsrp: {}, total: {}, mr_good: {}, mr_good_rate: {}>'.format(
            self.area, self.date, self.is_800, self.avg_rsrp, self.total, self.mr_good, self.mr_good_rate)
db.create_all()

# def draw_bar():
#     c = (
#         Bar()
#             .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#             .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
#             .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
#             .set_global_opts(title_opts=opts.TitleOpts(title="柱状图示例", subtitle="A,B商家销售数据对比"))
#     )
#     return c

def draw_bar(y_name,y_data,x_axis,title,subtitle):
    c = (
        Bar()
            .add_xaxis(x_axis)
            .add_yaxis(y_name,y_data)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=subtitle))
    )
    return c


def draw_line(x_axis,y_name,y_data):
    c = (
        Line()
            .add_xaxis(xaxis_data=x_axis)
            .add_yaxis(
            series_name=y_name,
            y_axis=y_data,
            symbol="circle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=4)
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    )
    return c


@app.route("/")
def show_index():
    return render_template('kpi_index.html')


@app.route("/mr")
def show_mr_kpi():
    pro_data = db.session.execute('select area,round(sum(mr_good)/sum(total),4) from mr_detail group by area order by round(sum(mr_good)/sum(total),4) desc')
    pro_data = list(pro_data)
    pro_x_axis = [x[0] for x in pro_data]
    pro_y_data = [round(x[1]*100,2) for x in pro_data]
    pro = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    # city_data = db.session.execute("select area,date_time,round(sum(mr_good)/sum(total),4) from mr_detail where area like '曲靖市'  group by date_time order by round(sum(mr_good)/sum(total),4) desc")
    # city_data = list(city_data)
    # city_x_axis = [x[1] for x in city_data]
    # city_y_data = [round(x[2]*100,2) for x in city_data]
    # city = draw_line(city_x_axis, '曲靖全月MR指标', city_y_data)
    city1800 = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    city800 = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    zte800 = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    zte_all = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    eric800 = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    eric_all = draw_bar('各州市MR指标',pro_y_data,pro_x_axis,'全省MR指标','全省各州市MR指标对比')
    return render_template('mr_report.html', pro_options=pro.dump_options(), city_options=city.dump_options(),
                           city1800_options=city1800.dump_options(), city800_options=city800.dump_options(),
                           zte800_options=zte800.dump_options(), zte_all_options=zte_all.dump_options(),
                           eric800_options=eric800.dump_options(), eric_all_options=eric_all.dump_options())


if __name__ == "__main__":
    app.run()
