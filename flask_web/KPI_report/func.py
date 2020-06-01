from exts import db
from models import Tousu
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie

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


def put2base(complaint_info,session3):
    if complaint_info['country'] == '0':
        lsit1 = ['富源', '宣威', '马龙', '陆良', '麒麟', '罗平', '师宗', '沾益', '会泽']
        conlist = filter(lambda x: x in complaint_info['content'], lsit1)
        cn_list = list(conlist)
        if cn_list:
            complaint_info['country'] = cn_list[0]
        else:
            conlist = filter(lambda x: x in complaint_info['result'], lsit1)
            cn_list = list(conlist)
            if cn_list:
                complaint_info['country'] = cn_list[0]
            else:
                complaint_info['country'] = '未知'
    else:
        dict_ct = {'1': '沾益', '2': '马龙', '3': '陆良', '4': '师宗', '5': '罗平', '6': '宣威', '7': '会泽', '8': '富源', '9': '麒麟'}
        complaint_info['country'] = dict_ct[complaint_info['country']]
    if complaint_info['town'] == '':
        if complaint_info['country'] == '0' or complaint_info['country'] == '未知':
            complaint_info['town'] = '未知'
        else:
            a = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if complaint_info['country'] not in a:
                f = open('E:/JupyterServer/KPI_report/dict乡镇.txt', 'r')
                a = f.read()
                dict_torw = eval(a)
                f.close()
                tmplist = filter(lambda x: x in complaint_info['content'], dict_torw[complaint_info['country']])
                newlist = list(tmplist)
                if newlist:
                    complaint_info['town'] = newlist[0]
                else:
                    complaint_info['town'] = '未知'
    dict_B = {'0': '未知',
                  '1': '弱覆盖',
                  '2': '无覆盖',
                  '3': '基站故障',
                  '4': '光缆故障',
                  '5': '用户终端故障',
                  '6': '容量问题',
                  '7': '优化问题',
                  '8': '达量限速',
                  '9': '其他'}
    complaint_info['res'] = dict_B[complaint_info['res']]
    dict_quyu = {'0': '未知',
                 '1': '城区',
                 '2': '乡镇',
                 '3': '农村', }
    complaint_info['area'] = dict_quyu[complaint_info['area']]
    dict_quyuxilei = {'0': '未知',
                      '1': '住宅小区',
                      '2': '厂矿企业',
                      '3': '政府机关单位',
                      '4': '商业区',
                      '5': '学校',
                      '6': '医院',
                      '7': '宾馆酒店',
                      '8': '交通枢纽',
                      '9': '娱乐场所',
                      '10': '乡镇',
                      '11': '自然村'}
    complaint_info['area_fenlei'] = dict_quyuxilei[complaint_info['area_fenlei']]
    dict_measure = {'0': '未知',
                      '1': '处理基站故障',
                      '2': '优化调整',
                      '3': '基站扩容',
                      '4': '基站建设',
                      '5': '使用WIFI替代',
                      '6': '用户自行处理',
                      '7': '网络正常无需处理',
                      '8': '非本期间故障无法处理',
                      '9': '开通volte替代'}
    complaint_info['measure']=dict_measure[complaint_info['measure']]
    user1 = Tousu(工单流水号=complaint_info['serial_number'],
                  区域=complaint_info['area'],
                  投诉内容=complaint_info['content'],
                  处理结果=complaint_info['result'],
                  区县=complaint_info['country'],
                  乡镇=complaint_info['town'],
                  我方办结原因=complaint_info['res'],
                  经度=complaint_info['lon'],
                  纬度=complaint_info['lat'],
                  关联基站代码=complaint_info['bts_id'],
                  关联基站名称=complaint_info['bts_name'],
                  关联自然村_小区名=complaint_info['village'],
                  区域细类=complaint_info['area_fenlei'],
                  解决措施=complaint_info['measure'])
    session3.add(user1)
    session3.commit()
    session3.close()

def updata2base(complaint_info,session3):
    dict_pd = {}
    if complaint_info['country'] == '0':
        lsit1 = ['富源', '宣威', '马龙', '陆良', '麒麟', '罗平', '师宗', '沾益', '会泽']
        conlist = filter(lambda x: x in complaint_info['content'], lsit1)
        cn_list = list(conlist)
        if cn_list:
            dict_pd['区县'] = cn_list[0]
        else:
            conlist = filter(lambda x: x in complaint_info['result'], lsit1)
            cn_list = list(conlist)
            if cn_list:
                dict_pd['区县'] = cn_list[0]

    else:
        dict_ct = {'1': '沾益', '2': '马龙', '3': '陆良', '4': '师宗', '5': '罗平', '6': '宣威', '7': '会泽', '8': '富源',
                   '9': '麒麟'}
        complaint_info['country'] = dict_ct.get(complaint_info['country'])
        dict_pd['区县'] = complaint_info['country']
    if complaint_info['town'] == '':
        if dict_pd:
            a = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if complaint_info['country'] not in a:
                f = open('E:/JupyterServer/KPI_report/dict乡镇.txt', 'r')
                a = f.read()
                dict_torw = eval(a)
                f.close()
                tmplist = filter(lambda x: x in complaint_info['content'], dict_torw[dict_pd["区县"]])
                newlist = list(tmplist)
                if newlist:
                    dict_pd['乡镇'] = newlist[0]
                else:
                    dict_pd['乡镇'] = '未知'
    else:
        dict_pd['乡镇'] = complaint_info['town']
    if complaint_info['res'] != '0':
        dict_B = {'0': '未知',
                  '1': '弱覆盖',
                  '2': '无覆盖',
                  '3': '基站故障',
                  '4': '光缆故障',
                  '5': '用户终端故障',
                  '6': '容量问题',
                  '7': '优化问题',
                  '8': '达量限速',
                  '9': '其他'}
        dict_pd['我方办结原因'] = dict_B[complaint_info['res']]
    if complaint_info['area'] != '0':
        dict_quyu = {'0': '未知',
                     '1': '城区',
                     '2': '乡镇',
                     '3': '农村', }
        dict_pd['区域'] = dict_quyu[complaint_info['area']]
    if complaint_info['area_fenlei'] != '0':
        dict_quyuxilei = {'0': '未知',
                          '1': '住宅小区',
                          '2': '厂矿企业',
                          '3': '政府机关单位',
                          '4': '商业区',
                          '5': '学校',
                          '6': '医院',
                          '7': '宾馆酒店',
                          '8': '交通枢纽',
                          '9': '娱乐场所',
                          '10': '乡镇',
                          '11': '自然村'}
        dict_pd['区域细类'] = dict_quyuxilei[complaint_info['area_fenlei']]
    if complaint_info['measure'] != '0':
        dict_measure = {'0': '未知',
                        '1': '处理基站故障',
                        '2': '优化调整',
                        '3': '基站扩容',
                        '4': '基站建设',
                        '5': '使用WIFI替代',
                        '6': '用户自行处理',
                        '7': '网络正常无需处理',
                        '8': '非本期间故障无法处理',
                        '9': '开通volte替代'}
        dict_pd['解决措施'] = dict_measure[complaint_info['measure']]
    if complaint_info['lon'] != '':
        dict_pd['经度'] = complaint_info['lon']
    if complaint_info['lat'] != '':
        dict_pd['纬度'] = complaint_info['lat']
    if complaint_info['bts_id'] != '':
        dict_pd['关联基站代码'] = complaint_info['bts_id']
    if complaint_info['bts_name'] != '':
        dict_pd['关联基站名称'] = complaint_info['bts_name']
    if complaint_info['village'] != '':
        dict_pd['关联自然村_小区名'] = complaint_info['village']
    dict_pd['处理结果']=complaint_info['result']
    for k, v in dict_pd.items():
        session3.execute(
            r'update tousu set {k}="{v}"where 工单流水号="{id}"'.format(k=k, v=v, id=complaint_info['serial_number']))
        session3.commit()
        session3.close()