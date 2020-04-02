from flask import Flask
from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
from pyecharts.faker import Faker

app = Flask(__name__, static_folder="templates")
app.debug = True

def draw_bar():
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
            .set_global_opts(title_opts=opts.TitleOpts(title="柱状图示例", subtitle="A,B商家销售数据对比"))
    )
    return c


def draw_line():
    c = (
        Line()
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(xaxis_data=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
            .add_yaxis(
            series_name="话务量",
            y_axis=[820, 932, 901, 934, 1290, 1330, 1320],
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="流量",
            y_axis=[620, 765, 710, 775, 900, 810, 1150],
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    return c


def draw_pie():
    c = (
        Pie()
            .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def draw_bar_over_line():
    x_data = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    bar = (
            Bar(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="蒸发量",
                yaxis_data=[2.0,4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name="降水量",
                yaxis_data=[ 2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3 ],
                label_opts=opts.LabelOpts(is_show=False),
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name="温度",
                    type_="value",
                    min_=0,
                    max_=25,
                    interval=5,
                    axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                )
            )
                .set_global_opts(
                    tooltip_opts=opts.TooltipOpts(
                        is_show=True, trigger="axis", axis_pointer_type="cross"
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                ),
                    yaxis_opts=opts.AxisOpts(
                        name="水量",
                        type_="value",
                        min_=0,
                        max_=250,
                        interval=50,
                        axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
            )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
        series_name="平均温度",
        yaxis_index=1,
        y_axis=[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
        label_opts=opts.LabelOpts(is_show=False),
        )
    )

    c = bar.overlap(line)
    return c

@app.route("/")
def show_pyecharts():
    bar = draw_bar()
    line = draw_line()
    pie = draw_pie()
    bar_line = draw_bar_over_line()
    return render_template('show_pyecharts.html', bar_options=bar.dump_options(), line_options=line.dump_options(),
                           pie_options=pie.dump_options(), bar_line_options=bar_line.dump_options())

if __name__ == "__main__":
    app.run()
