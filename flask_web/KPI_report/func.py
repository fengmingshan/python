from exts import db
from models import Tousu,Rrc_recon,Rrc_rate,Erab_drop,Vol_connect,Vol_drop
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
import time
from datetime import datetime

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
def draw_bar2(y_name1,y_name2,y_data1,y_data2,x_axis,title):
    c = (
        Bar()
            .add_xaxis(x_axis)
            .add_yaxis(y_name1,y_data1,category_gap="60%")
            .add_yaxis(y_name2,y_data2,category_gap="60%")
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

def draw_bar_reversal(x_axis,y_data,y_name,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name,y_data)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
        legend_opts=opts.LegendOpts(
            pos_right="right",
            pos_top="20"
        ),
        title_opts=opts.TitleOpts(title=title),
        )
    )
    return c


def draw_bar2_reversal(x_axis,y_data1,y_name1,y_data2,y_name2,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1,y_data1)
        .add_yaxis(y_name2, y_data2)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    return c

def draw_bar_stack(x_axis,y_name1,y_data1,y_name2,y_data2,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1, y_data1, stack="stack1")
        .add_yaxis(y_name2, y_data2, stack="stack1")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title=title),
                         xaxis_opts=opts.AxisOpts(
                             axislabel_opts={"interval": "0"}
                         )
        )
    )
    return c

def draw_bar_stack_3(x_axis,y_name1,y_data1,y_name2,y_data2,y_name3,y_data3,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1, y_data1, stack="stack1")
        .add_yaxis(y_name2, y_data2, stack="stack1")
        .add_yaxis(y_name3, y_data3, stack="stack1")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        legend_opts=opts.LegendOpts(
            pos_left="right",
            pos_top="20"
        ),
        title_opts=opts.TitleOpts(
        title=title,
        pos_top="0"
        ),
        )
    )
    return c

def draw_bar_stack_4(x_axis,y_name1,y_data1,y_name2,y_data2,y_name3,y_data3,y_name4,y_data4,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1, y_data1, stack="stack1")
        .add_yaxis(y_name2, y_data2, stack="stack1")
        .add_yaxis(y_name3, y_data3, stack="stack1")
        .add_yaxis(y_name4, y_data4, stack="stack1")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        legend_opts=opts.LegendOpts(
            pos_left="left",
            pos_top="20"
        ),      
        title_opts=opts.TitleOpts(title=title))
    )
    return c

def draw_bar_stack_5(x_axis,y_name1,y_data1,y_name2,y_data2,y_name3,y_data3,y_name4,y_data4,y_name5,y_data5,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1, y_data1, stack="stack1")
        .add_yaxis(y_name2, y_data2, stack="stack1")
        .add_yaxis(y_name3, y_data3, stack="stack1")
        .add_yaxis(y_name4, y_data4, stack="stack1")
        .add_yaxis(y_name5, y_data5, stack="stack1")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        legend_opts=opts.LegendOpts(
            pos_left="left",
            pos_top="20"
        ),    
        title_opts=opts.TitleOpts(title=title))
    )
    return c

def draw_bar_stack_6(x_axis,y_name1,y_data1,y_name2,y_data2,y_name3,y_data3,y_name4,y_data4,y_name5,y_data5,y_name6,y_data6,title):
    c = (
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(y_name1, y_data1, stack="stack1")
        .add_yaxis(y_name2, y_data2, stack="stack1")
        .add_yaxis(y_name3, y_data3, stack="stack1")
        .add_yaxis(y_name4, y_data4, stack="stack1")
        .add_yaxis(y_name5, y_data5, stack="stack1")
        .add_yaxis(y_name6, y_data6, stack="stack1")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        legend_opts=opts.LegendOpts(
            pos_right="right",
            pos_top="20"
        ),
        title_opts=opts.TitleOpts(
        title=title,
        pos_top="0"
        ),
        )
    )
    return c

def draw_pie(x_data, y_data, series_name, title):
    data_pair = [list(z) for z in zip(x_data, y_data)]
    data_pair.sort(key=lambda x: x[1])
    c= (
        Pie(init_opts=opts.InitOpts(width="1600px", height="1000px"))
            .add(
            series_name= series_name,
            data_pair=[list(z) for z in zip(x_data, y_data)],
            label_opts=opts.LabelOpts(is_show=True, position="outside"),
            )
            .set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_left="left",
                pos_top="20",
                orient="vertical"
            ),
            title_opts=opts.TitleOpts(
                title=title,
                pos_left="center",
                pos_top="0",
                title_textstyle_opts=opts.TextStyleOpts(color="#6a98ab"),
            ),
            )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
            )
    )
    return c


def draw_line3(title,x_axis,y_name1,y_data1,y_name2,y_data2,y_name3,y_data3):
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
            .add_yaxis(
            series_name=y_name3,
            y_axis=y_data3,
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
    )
    return c

def draw_mixed_line_bar(xdate, line_ydate,line_name, bar_ydate, bar_name):
    bar = (
        Bar(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add_xaxis(xaxis_data= xdate)
        .add_yaxis(
            series_name= bar_name,
            yaxis_data = bar_ydate,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name= line_name,
                type_="value",
                min_=0,
                max_=100,
                interval=10,
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
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
                name=bar_name,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data= xdate)
        .add_yaxis(
            series_name= line_name,
            yaxis_index=1,
            y_axis=line_ydate,
            label_opts=opts.LabelOpts(is_show=False),
        )
    )
    c = bar.overlap(line)
    return c

def updata_rrc_reconn(complaint_info,session3):
    now_week = datetime.now().isocalendar()[1]-1
    dict_pd = {}
    dict_pd['重建原因'] = complaint_info['cause']
    dict_pd['处理措施'] = complaint_info['measure']
    dict_pd['处理人'] = complaint_info['handler']
    dict_pd['处理详情'] = complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update rrc重建比例top小区 set {k}="{v}"where 站号="{id}" and 小区号="{cell}" and 周 = "{now_week}"'.format(k=k, v=v, id=complaint_info['eNodbe_number'],cell=complaint_info['eNodbe_cell'],now_week=now_week))
        session3.commit()
        session3.close()


def updata_rrc_rate(complaint_info,session3):
    now_week = datetime.now().isocalendar()[1] - 1
    dict_pd = {}
    dict_pd['重建原因'] = complaint_info['cause']
    dict_pd['处理措施'] = complaint_info['measure']
    dict_pd['处理人'] = complaint_info['handler']
    dict_pd['处理详情'] = complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update rrc重建成功率top小区 set {k}="{v}"where 站号="{id}" and 小区号="{cell}" and 周 = "{now_week}"'.format(k=k, v=v, id=complaint_info['eNodbe_number'],cell= complaint_info['eNodbe_cell'],now_week=now_week))
        session3.commit()
        session3.close()

def updata_erab_drop(complaint_info,session3):
    now_week = datetime.now().isocalendar()[1] - 1
    dict_pd = {}
    dict_pd['掉线原因'] = complaint_info['cause']
    dict_pd['处理措施'] = complaint_info['measure']
    dict_pd['处理人'] = complaint_info['handler']
    dict_pd['处理详情'] = complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update rrc重建成功率top小区 set {k}="{v}"where 站号="{id}" and 小区号="{cell}" and 周 = "{now_week}"'.format(k=k, v=v,
                                                                                                              id=
                                                                                                              complaint_info[
                                                                                                                  'eNodbe_number'],
                                                                                                              cell=
                                                                                                              complaint_info[
                                                                                                                  'eNodbe_cell'],
                                                                                                              now_week=now_week))
        session3.commit()
        session3.close()

def updata_vol_connect(complaint_info, session3):
    now_week = datetime.now().isocalendar()[1] - 1
    dict_pd = {}
    dict_pd['未接通原因'] = complaint_info['cause']
    dict_pd['处理措施'] = complaint_info['measure']
    dict_pd['处理人'] = complaint_info['handler']
    dict_pd['处理详情'] = complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update rrc重建成功率top小区 set {k}="{v}"where 站号="{id}" and 小区号="{cell}" and 周 = "{now_week}"'.format(k=k, v=v,
                                                                                                              id=
                                                                                                              complaint_info[
                                                                                                                  'eNodbe_number'],
                                                                                                              cell=
                                                                                                              complaint_info[
                                                                                                                  'eNodbe_cell'],
                                                                                                              now_week=now_week))
        session3.commit()
        session3.close()

def updata_vol_drop(complaint_info, session3):
    now_week = datetime.now().isocalendar()[1] - 1
    dict_pd = {}
    dict_pd['掉话原因'] = complaint_info['cause']
    dict_pd['处理措施'] = complaint_info['measure']
    dict_pd['处理人'] = complaint_info['handler']
    dict_pd['处理详情'] = complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update rrc重建成功率top小区 set {k}="{v}"where 站号="{id}" and 小区号="{cell}" and 周 = "{now_week}"'.format(k=k, v=v,
                                                                                                              id=
                                                                                                              complaint_info[
                                                                                                                  'eNodbe_number'],
                                                                                                              cell=
                                                                                                              complaint_info[
                                                                                                                  'eNodbe_cell'],
                                                                                                              now_week=now_week))
        session3.commit()
        session3.close()
