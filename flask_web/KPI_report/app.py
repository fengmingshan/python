# -*- coding: utf-8 -*-

from flask import Flask, url_for, request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tousu
from forms import Complaint_form, Select_form
from config import Config
from func import draw_bar, draw_line3, draw_line2, draw_line, draw_pie, draw_bar_reversal, draw_bar2_reversal, \
    draw_bar_stack_3, draw_bar_stack, draw_bar_stack_6, draw_bar_stack_4, draw_bar_stack_5
from func import put2base, updata2base

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.config.from_object(Config)

engine_mr = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/mr_report?charset=utf8", pool_recycle=1800)
engine_cqi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/cqi_report?charset=utf8", pool_recycle=1800)
engine_tousu = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/qjwx_tousu?charset=utf8",
                             pool_recycle=1800)
engine_kpi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/kpi_report?charset=utf8", pool_recycle=1800)
engine_rrc = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/rrc_reconnect?charset=utf8",
                           pool_recycle=1800)
engine_handover = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/hand_over?charset=utf8",
                                pool_recycle=1800)

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


@app.route("/")
def show_index():
    month = session_mr.execute("select DISTINCT month(date_time) as 'month' from mr_summary")
    month = list(month)
    month = [x.month for x in month]
    month = max(month)
    return render_template('kpi_index.html', month=month)


@app.route("/mr")
def show_mr_kpi():
    month = session_mr.execute("select DISTINCT month(date_time) from mr_summary")
    month = list(month)
    month = [x[0] for x in month]
    month = max(month)

    pro_data = session_mr.execute(
        "select area,round(sum(mr_good)/sum(total),4)*100 from mr_summary where static_zone = '全市' and month(date_time) = {month} group by area order by round(sum(mr_good)/sum(total),4)*100 desc".format(
            month=month))
    pro_data = list(pro_data)
    pro_x_axis = [x[0] for x in pro_data]
    pro_y_data = [float(x[1]) for x in pro_data]
    pro = draw_bar('全网', pro_y_data, pro_x_axis, '全省各州市MR全网指标对比')

    pro_data_not800 = session_mr.execute(
        "select area,round(sum(mr_good)/sum(total),4)*100 from mr_summary where static_zone = '1800M' and month(date_time) = {month} group by area order by round(sum(mr_good)/sum(total),4)*100 desc".format(
            month=month))
    pro_data_not800 = list(pro_data_not800)
    pro_x_axis_not800 = [x[0] for x in pro_data_not800]
    pro_y_data_not800 = [x[1] for x in pro_data_not800]
    pro_not800 = draw_bar('L1800', pro_y_data_not800, pro_x_axis_not800, '全省各州市L1800网络MR指标')

    pro_data_800 = session_mr.execute(
        "select area,round(sum(mr_good)/sum(total),4)*100 from mr_summary where static_zone = '800M' and month(date_time) = {month} group by area order by round(sum(mr_good)/sum(total),4)*100 desc".format(
            month=month))
    pro_data_800 = list(pro_data_800)
    pro_x_axis_800 = [x[0] for x in pro_data_800]
    pro_y_data_800 = [x[1] for x in pro_data_800]
    pro_800 = draw_bar('800M', pro_y_data_800, pro_x_axis_800, '全省各州市800M网络MR指标')

    qj_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '全市' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    qj_data = list(qj_data)
    qj_x_axis = [x[0] for x in qj_data]
    qj_y_data = [round(x[1] * 100, 2) for x in qj_data]
    qj1800_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '1800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    qj1800_data = list(qj1800_data)
    qj1800_y_data = [round(x[1] * 100, 2) for x in qj1800_data]
    qj800_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    qj800_data = list(qj800_data)
    qj800_y_data = [round(x[1] * 100, 2) for x in qj800_data]
    qj = draw_line3('曲靖全市两网指标对比', qj_x_axis, '曲靖全市', qj_y_data, '曲靖1800M', qj1800_y_data, '曲靖800M', qj800_y_data)

    zte_all_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '中兴' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    zte_all_data = list(zte_all_data)
    zte_all_x_axis = [x[0] for x in zte_all_data]
    zte_all_y_data = [round(x[1] * 100, 2) for x in zte_all_data]
    zte1800_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '中兴1800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    zte1800_data = list(zte1800_data)
    zte1800_y_data = [round(x[1] * 100, 2) for x in zte1800_data]
    zte800_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '中兴800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    zte800_data = list(zte800_data)
    zte800_y_data = [round(x[1] * 100, 2) for x in zte800_data]
    zte = draw_line3('中兴两网指标对比', zte_all_x_axis, '中兴全网MR指标', zte_all_y_data, '中兴1800M', zte1800_y_data, '中兴800M',
                     zte800_y_data)

    eric800_data = session_mr.execute(
        "select date_time,mr_good_rate from mr_summary where area = '曲靖市' and static_zone = '爱立信800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    session_mr.close()
    eric800_data = list(eric800_data)
    eric800_x_axis = [x[0] for x in eric800_data]
    eric800_y_data = [round(x[1] * 100, 2) for x in eric800_data]
    eric_zte = draw_line2('爱立信中兴800M指标对比', eric800_x_axis, '爱立信800M', eric800_y_data, '中兴800M', zte800_y_data)
    return render_template('mr_report.html', pro_options=pro.dump_options(),
                           pro_not800_options=pro_not800.dump_options(),
                           pro_800_options=pro_800.dump_options(), qj_options=qj.dump_options(),
                           zte_options=zte.dump_options(), eric_zte_options=eric_zte.dump_options())


@app.route("/cqi")
def show_cqi_kpi():
    month = session_cqi.execute("select DISTINCT month(date_time) from cqi_summary")
    month = list(month)
    month = [x[0] for x in month]
    month = max(month)

    pro_data = session_cqi.execute(
        "select area,round(abpve7_rate,4)*100 from cqi_summary where static_zone = '全市' and month(date_time) = {month} group by area order by round(abpve7_rate,4)*100 desc".format(
            month=month))
    pro_data = list(pro_data)
    pro_x_axis = [x[0] for x in pro_data]
    pro_y_data = [x[1] for x in pro_data]
    pro = draw_bar('全网', pro_y_data, pro_x_axis, '全省各州市CQI全网指标对比')

    pro_data_not800 = session_cqi.execute(
        "select area,round(abpve7_rate,4)*100 from cqi_summary where static_zone = '1800M' and month(date_time) = {month} group by area order by round(abpve7_rate,4)*100 desc".format(
            month=month))
    pro_data_not800 = list(pro_data_not800)
    pro_x_axis_not800 = [x[0] for x in pro_data_not800]
    pro_y_data_not800 = [x[1] for x in pro_data_not800]
    pro_not800 = draw_bar('L1800', pro_y_data_not800, pro_x_axis_not800, '全省各州市L1800网络CQI指标')

    pro_data_800 = session_cqi.execute(
        "select area,round(abpve7_rate,4)*100 from cqi_summary where static_zone = '800M' and month(date_time) = {month} group by area order by round(abpve7_rate,4)*100 desc".format(
            month=month))
    pro_data_800 = list(pro_data_800)
    pro_x_axis_800 = [x[0] for x in pro_data_800]
    pro_y_data_800 = [x[1] for x in pro_data_800]
    pro_800 = draw_bar('800M', pro_y_data_800, pro_x_axis_800, '全省各州市800M网络CQI指标')

    qj_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '全市' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    qj_data = list(qj_data)
    qj_x_axis = [x[0] for x in qj_data]
    qj_y_data = [round(x[1] * 100, 2) for x in qj_data]
    qj1800_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '1800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    qj1800_data = list(qj1800_data)
    qj1800_y_data = [round(x[1] * 100, 2) for x in qj1800_data]
    qj800_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    qj800_data = list(qj800_data)
    qj800_y_data = [round(x[1] * 100, 2) for x in qj800_data]
    qj = draw_line3('曲靖全市两网CQI指标对比', qj_x_axis, '曲靖全月', qj_y_data, '曲靖1800M', qj1800_y_data, '曲靖800M', qj800_y_data)

    zte_all_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '中兴' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    zte_all_data = list(zte_all_data)
    zte_all_x_axis = [x[0] for x in zte_all_data]
    zte_all_y_data = [round(x[1] * 100, 2) for x in zte_all_data]
    zte1800_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '中兴1800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    zte1800_data = list(zte1800_data)
    zte1800_y_data = [round(x[1] * 100, 2) for x in zte1800_data]
    zte800_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '中兴800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    zte800_data = list(zte800_data)
    zte800_y_data = [round(x[1] * 100, 2) for x in zte800_data]
    zte = draw_line3('中兴两网CQI指标对比', zte_all_x_axis, '中兴全网CQI指标', zte_all_y_data, '中兴1800M', zte1800_y_data, '中兴800M',
                     zte800_y_data)

    eric800_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '爱立信800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    session_cqi.close()
    eric800_data = list(eric800_data)
    eric800_x_axis = [x[0] for x in eric800_data]
    eric800_y_data = [round(x[1] * 100, 2) for x in eric800_data]
    eric_zte = draw_line2('爱立信中兴800MCQI指标对比', eric800_x_axis, '爱立信800M', eric800_y_data, '中兴800M', zte800_y_data)
    return render_template('cqi_report.html', pro_options=pro.dump_options(),
                           pro_not800_options=pro_not800.dump_options(),
                           pro_800_options=pro_800.dump_options(), qj_options=qj.dump_options(),
                           zte_options=zte.dump_options(), eric_zte_options=eric_zte.dump_options())


@app.route("/cell", methods=['GET', 'POST'])
def show_cell_traffic():
    select_form = Select_form()
    if request.method == 'POST':
        if select_form.validate_on_submit():
            bts_info = request.form.to_dict()
            eNodeB = bts_info.get('eNodeB')
            Cell = bts_info.get('cellid')
            Month = bts_info.get('month')
            Date = bts_info.get('date')
            rrc_user = session_kpi.execute(
                "SELECT Start_time, Avg_number_of_UE_in_RRc from zte_hour WHERE month(zte_hour.Start_time) = {month} and day(zte_hour.Start_time) = {day} and eNodeB = {enb} and cell = {cell} ORDER BY zte_hour.Start_time asc".format(
                    month=Month, day=Date, enb=eNodeB, cell=Cell))
            rrc_user = list(rrc_user)
            rrc_user_x_axis = [x[0] for x in rrc_user]
            rrc_user_y_data = [x[1] for x in rrc_user]
            rrc_user_bar = draw_bar('RRC连接用户数', rrc_user_y_data, rrc_user_x_axis, '小区RRC连接用户数')
            return render_template('cell_traffic.html', rrc_user_options=rrc_user_bar.dump_options())
    return render_template('select_cell.html', form=select_form)


@app.route("/rrc")
def show_rrc_kpi():
    qtem_rrc = session_kpi.execute(
        "select 时间,RRC连接重建比例 from(select 时间,RRC连接重建比例 from kpi_summary where 厂家='不区分厂家' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [x.时间 for x in qtem_rrc]
    qtem_rrc_data = [x.RRC连接重建比例 for x in qtem_rrc]
    qw_rrc = draw_line(qtem_rrc_x_axis, '全网RRC重建比例', qtem_rrc_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,RRC连接重建比例 from(select 时间,RRC连接重建比例 from kpi_summary where 厂家='中兴' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [x[1] for x in item_rrc1]
    item_rrc2 = session_kpi.execute(
        "select 时间,RRC连接重建比例 from(select 时间,RRC连接重建比例 from kpi_summary where 厂家='中兴' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc2 = list(item_rrc2)
    item_rrc_n800_data = [x[1] for x in item_rrc2]
    zte_rrc = draw_line2('中兴两网指标对比', item_rrc_x_axis, '中兴800M', item_rrc_800_data, '中兴非800M', item_rrc_n800_data)

    rtem_rrc = session_kpi.execute(
        "select 时间,RRC连接重建比例 from(select 时间,RRC连接重建比例 from kpi_summary where 厂家='爱立信' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data = [x[1] for x in rtem_rrc1]
    rtem_rrc2 = session_kpi.execute(
        "select 时间,RRC连接重建比例 from(select 时间,RRC连接重建比例 from kpi_summary where 厂家='爱立信' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc2 = list(rtem_rrc2)
    rtem_rrc_n800_data = [x[1] for x in rtem_rrc2]
    eri_rrc = draw_line2('爱立信两网指标对比', rtem_rrc_x_axis, '爱立信800M', rtem_rrc_800_data, '爱立信非800M', rtem_rrc_n800_data)

    htem_rrc = session_kpi.execute(
        "select 时间,RRC连接重建比例 from(select 时间,RRC连接重建比例 from kpi_summary where 厂家='华为' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    htem_rrc1 = list(htem_rrc)
    htem_rrc_x_axis = [x[0] for x in htem_rrc1]
    htem_rrc_data = [x[1] for x in htem_rrc1]
    hw_rrcc = draw_line(htem_rrc_x_axis, '华为', htem_rrc_data, '华为', )

    return render_template('rrc_cj_report.html', zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(), qw_rrc_options=qw_rrc.dump_options())


@app.route("/rrc_recon_top/", methods=['GET', 'POST'])
def show_rrc_recon_list():
    cur_week = session_rrc.execute("SELECT max(week(`日期`)) from `rrc重建`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_rrc.execute(
        "SELECT 站号, `小区号`, `小区名称`, `RRC重建请求数目`, a.rrc_recon_ratio, a.rrc_recon_count/b.rrc_recon_sum as '占全网比例' FROM (SELECT 站号, `小区号`, `小区名称`, week(`日期`) as 'week', `RRC重建请求数目`, `RRC重建立比例` as 'rrc_recon_ratio', `RRC重建请求数目` as 'rrc_recon_count' from `rrc重建`) as a, (SELECT sum(`RRC重建请求数目`) as 'rrc_recon_sum' from `rrc重建`) as b WHERE a.`week` = {cur_week} ORDER BY a.rrc_recon_count/b.rrc_recon_sum DESC LIMIT 20".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.站号 for x in top_cells]
    top_cells_cell = [x.小区号 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    return render_template('rrc_recon_list.html', top_cells_info=top_cells_info, top_cells_name=top_cells_name)


@app.route("/rrc_recon_top/<cell_info>", methods=['GET', 'POST'])
def show_rrc_recon_detail(cell_info):
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    weeks = session_rrc.execute("SELECT DISTINCT `周` from `rrc重建`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week =max(weeks)

    recon_ratio = session_rrc.execute(
        "SELECT `小区名称`,站号, `小区号`, `RRC重建立比例`, `RRC重建请求数目`, `RRC连接重建成功率`,`切换失败触发的RRC重建立请求次数`, `其它原因触发的RRC重建立请求次数`, `重配失败触发的RRC重建立请求次数` FROM `rrc重建` where 站号 = {enb} and `小区号` ={cell} and `周` = {week}".format(
            enb=enb, cell=cell, week=cur_week))
    recon_ratio = list(recon_ratio)
    cell_name = recon_ratio[0].小区名称
    ratio =  [x.RRC重建立比例 for x in recon_ratio]
    ratio_sec= [x.RRC连接重建成功率 for x in recon_ratio]
    recon_count = [x.RRC重建请求数目 for x in recon_ratio]
    recon_ratio_chart = draw_line2(' ',weeks,'RRC重建比例', ratio, 'RRC连接重建成功率',ratio_sec)
    recon_count_chart = draw_bar('RRC重建请求次数', recon_count,  weeks, 'RRC重建次数',)

    recon_reason = recon_ratio[0][6:]
    recon_reason_chart = draw_pie(['切换失败','其它原因','重配失败'],recon_reason,'RRC重建原因:','RRC重建原因')

    ho_count = session_handover.execute(
        "SELECT `邻区`, `切换出请求总次数`,`切换出成功次数`, `切换出失败次数`, `切换出执行失败次数_源侧发生重建立`, `切换出执行失败次数_等待UECONTEXTRELEASE消息超时`, `切换出执行失败次数_其它原因`, `切换出准备失败次数_等待切换响应定时器超时`, `切换出准备失败次数_目标侧准备失败`, `切换出准备失败次数_其它原因`, `切换出准备失败次数_源侧发生重建立`, `切换出准备失败次数_用户未激活`, `切换出准备失败次数_传输资源受限`,`切换入成功次数`, `切换入失败次数`, `切换入执行失败次数_RRC重配完成超时`, `切换入执行失败次数_源侧取消切换`, `切换入执行失败次数_目标侧发生重建立`, `切换入执行失败次数_其他原因`, `切换入准备失败次数_资源分配失败`, `切换入准备失败次数_源侧取消切换`, `切换入准备失败次数_目标侧发生重建立`, `切换入准备失败次数_传输资源受限`, `切换入准备失败次数_其它原因` FROM `邻区切换` WHERE eNodeB = {enb} and `小区` = {cell} and `周`= {week}  and `切换出失败次数`>0  order by 切换出请求总次数 asc limit 40".format(
            enb=enb, cell=cell, week=cur_week))
    ho_count = list(ho_count)
    ho_count_ne = [x[0] for x in ho_count]
    ho_sec_out = [x[2] for x in ho_count]
    ho_fail_out = [x[3] for x in ho_count]
    ho_re_fail_1 = [x[7] for x in ho_count]
    ho_re_fail_2 = [x[8] for x in ho_count]
    ho_re_fail_3 = [x[9] for x in ho_count]
    ho_re_fail_4 = [x[10] for x in ho_count]
    ho_re_fail_5 = [x[11] for x in ho_count]
    ho_re_fail_6 = [x[12] for x in ho_count]
    ho_do_fail_1= [x[4] for x in ho_count]
    ho_do_fail_2 = [x[5] for x in ho_count]
    ho_do_fail_3 = [x[6] for x in ho_count]
    ho_sec_in = [x[13] for x in ho_count]
    ho_fail_in = [x[14] for x in ho_count]
    ho_do_in_1 = [x[15] for x in ho_count]
    ho_do_in_2 = [x[16] for x in ho_count]
    ho_do_in_3 = [x[17] for x in ho_count]
    ho_do_in_4 = [x[18] for x in ho_count]
    ho_re_in_1 = [x[19] for x in ho_count]
    ho_re_in_2 = [x[20] for x in ho_count]
    ho_re_in_3 = [x[21] for x in ho_count]
    ho_re_in_4 = [x[22] for x in ho_count]
    ho_re_in_5 = [x[23] for x in ho_count]
    ho_count_secc_chart = draw_bar_stack(ho_count_ne,'切换出成功次数',ho_sec_out,'切换出失败次数',ho_fail_out,'切换分析')
    HO_count_chart = draw_bar_stack_6(['' for x in range(len(ho_count_ne))],'等待切换响应定时器超时',ho_re_fail_1,'目标侧准备失败',ho_re_fail_2,'传输资源受限',ho_re_fail_6,'源侧发生重建立',ho_re_fail_4,'用户未激活',ho_re_fail_5,'其它原因',ho_re_fail_3,'切换出准备失败', )
    ho_do_fail_chart = draw_bar_stack_3(['' for x in range(len(ho_count_ne))],'源侧发生重建立',ho_do_fail_1,'等待UECONTEXTRELEASE消息超时',ho_do_fail_2,'其它原因',ho_do_fail_3,'切换出执行失败')
    ho_count_in_chart = draw_bar_stack(ho_count_ne, '切换入成功次数', ho_sec_in, '切换入失败次数', ho_fail_in, '切换分析')
    HO_do_in_chart = draw_bar_stack_4(['' for x in range(len(ho_count_ne))], 'RRC重配完成超时', ho_do_in_1, '源侧取消切换',
                                      ho_do_in_2, '目标侧发生重建立', ho_do_in_3, '其他原因', ho_do_in_4,  '切换入执行失败', )
    HO_re_in_chart = draw_bar_stack_5(['' for x in range(len(ho_count_ne))], '资源分配失败', ho_re_in_1, '源侧取消切换',
                                      ho_re_in_2, '目标侧发生重建立', ho_re_in_3, '传输资源受限', ho_re_in_4, '其它原因',
                                      ho_re_in_5, '切换入准备失败', )

    ho_distance = session_handover.execute(
        "SELECT a.`邻区`, b.distance from (SELECT `邻区`,`邻区关系`,`切换出请求总次数` FROM `邻区切换` WHERE eNodeB = {enb} and 小区 = {cell} and (`切换出请求总次数`>30 OR `切换入请求总次数`>30 OR `切换出成功次数`>30 OR `切换入成功次数`>30)) as a left JOIN  (SELECT relation,distance from `邻区距离`) as b ON a.`邻区关系`=b.relation order by a.`切换出请求总次数`".format(enb =enb ,cell = cell))
    ho_distance = list(ho_distance)
    distance_ce = [x.邻区 for x in ho_distance]
    df_distance = [x.distance for x in ho_distance]
    HO_distance_chart = draw_bar_reversal(distance_ce, df_distance, '邻区站点距离', ' ', )
    HO_distan_chart = draw_bar_reversal(['' for x in range(len(distance_ce))], df_distance, '邻区站点距离', ' ', )

    item_TA = session_kpi.execute(
        "select TA0_1,TA1_3,TA3_5,TA5_7,TA7_9,TA9_11,TA11_13,TA13_20,TA20_27,TA27_34,TA34_40,TA40_50,TA50_81,TA81_129,TA129_179 FROM zte_day_4  where 站号 = {} and 小区号 = {} ORDER BY 日期 DESC LIMIT 1".format(
            enb, cell))
    session_kpi.close()
    item_TA = list(item_TA)
    item_TA = list(item_TA[0])
    item_TA_x_axis = ['78.12m', '78~234m', '234~390m', '390~547m', '547~703m', '703~859m', '859~1015m', '1015~1562m',
                      '1562~2109m', '2109~2656m', '2656~3125m', '3125~3906m', '3906~6328m', '6328~10077m', '10077~13983m']
    item_TA_y_data = item_TA
    TA_dist_chart = draw_bar('TA分布',item_TA_y_data,item_TA_x_axis,'TA分布')

    rrc_rec = session_kpi.execute(
        "select 日期,系统内切换成功率 from(select 日期,系统内切换成功率 from zte_day_4 where 站号 = {} and 小区号 = {} order by 日期 DESC LIMIT 10)aa ORDER BY 日期 asc".format(
            enb, cell))
    session_kpi.close()
    rrc_rec = list(rrc_rec)
    rrc_rec_x_axis = [x[0] for x in rrc_rec]
    rec_ho_y_data = [round(x[1] * 100, 2) for x in rrc_rec]
    recon_kpi_chart = draw_line(rrc_rec_x_axis, ' ', rec_ho_y_data,'系统内切换成功率' )

    return render_template('rrc_recon_detail.html', cell_name = cell_name,rrc_recon_reason_chart_options=recon_reason_chart.dump_options(),
                           rrc_recon_ratio_chart_options=recon_ratio_chart.dump_options(),rrc_recon_count_chart_options=recon_count_chart.dump_options(),
                           ho_count_secc_chart_options=ho_count_secc_chart.dump_options(), HO_count_chart_options=HO_count_chart.dump_options(),
                           ho_do_fail_chart_options=ho_do_fail_chart.dump_options(),HO_distance_chart_options=HO_distance_chart.dump_options(),
                           ho_count_in_chart_options=ho_count_in_chart.dump_options(),HO_distan_chart_options=HO_distan_chart.dump_options(),
                           HO_do_in_chart_options=HO_do_in_chart.dump_options(),HO_re_in_chart_options=HO_re_in_chart.dump_options(),
                           TA_dist_chart_options=TA_dist_chart.dump_options(),recon_kpi_chart_options=recon_kpi_chart.dump_options())

@app.route("/success")
def show_rrc_success():
    qtem_rrc = session_kpi.execute(
        "select 时间,RRC连接重建成功率 from(select 时间,RRC连接重建成功率 from kpi_summary where 厂家='不区分厂家' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [x.时间 for x in qtem_rrc]
    qtem_rrc_data = [x.RRC连接重建成功率 for x in qtem_rrc]
    qw_rrc = draw_line(qtem_rrc_x_axis, '全网RRC重建成功率', qtem_rrc_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,RRC连接重建成功率 from(select 时间,RRC连接重建成功率 from kpi_summary where 厂家='中兴' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [x[1] for x in item_rrc1]
    item_rrc2 = session_kpi.execute(
        "select 时间,RRC连接重建成功率 from(select 时间,RRC连接重建成功率 from kpi_summary where 厂家='中兴' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc2 = list(item_rrc2)
    item_rrc_n800_data = [x[1] for x in item_rrc2]
    zte_rrc = draw_line2('中兴两网指标对比', item_rrc_x_axis, '中兴800M', item_rrc_800_data, '中兴非800M', item_rrc_n800_data)

    rtem_rrc = session_kpi.execute(
        "select 时间,RRC连接重建成功率 from(select 时间,RRC连接重建成功率 from kpi_summary where 厂家='爱立信' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data = [x[1] for x in rtem_rrc1]
    rtem_rrc2 = session_kpi.execute(
        "select 时间,RRC连接重建成功率 from(select 时间,RRC连接重建成功率 from kpi_summary where 厂家='爱立信' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc2 = list(rtem_rrc2)
    rtem_rrc_n800_data = [x[1] for x in rtem_rrc2]
    eri_rrc = draw_line2('爱立信两网指标对比', rtem_rrc_x_axis, '爱立信800M', rtem_rrc_800_data, '爱立信非800M', rtem_rrc_n800_data)

    htem_rrc = session_kpi.execute(
        "select 时间,RRC连接重建成功率 from(select 时间,RRC连接重建成功率 from kpi_summary where 厂家='华为' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    htem_rrc1 = list(htem_rrc)
    htem_rrc_x_axis = [x[0] for x in htem_rrc1]
    htem_rrc_data = [x[1] for x in htem_rrc1]
    hw_rrcc = draw_line(htem_rrc_x_axis, '华为', htem_rrc_data, '华为', )

    return render_template('rrc_success_report.html', zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(), qw_rrc_options=qw_rrc.dump_options())


@app.route("/rrc_rate_top/", methods=['GET', 'POST'])
def show_rrc_rate_list():
    cur_week = session_rrc.execute("SELECT max(`周`) from `rrc重建`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_rrc.execute(
        "SELECT 站号, `小区号`, `小区名称`, `RRC连接重建成功率`, `RRC重建请求数目`, `RRC重建失败数目`, b.all_failed_ratio - ((b.failed_sum-`RRC重建失败数目`)/(b.req_sum-`RRC重建请求数目`)) as '占全网比例', b.all_failed_ratio FROM (SELECT 站号, `小区号`, `小区名称`, week(`日期`) as 'week',`RRC连接重建成功率`, `RRC重建请求数目`, `RRC重建失败数目` FROM rrc重建) as a, (SELECT sum(`RRC重建请求数目`) as req_sum, sum(`RRC重建失败数目`) as failed_sum, round(sum(`RRC重建失败数目`)/sum(`RRC重建请求数目`),4) as all_failed_ratio FROM rrc重建) as b WHERE a.`week` = {cur_week} ORDER BY b.all_failed_ratio - ((b.failed_sum-`RRC重建失败数目`)/(b.req_sum-`RRC重建请求数目`)) desc LIMIT 20".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.站号 for x in top_cells]
    top_cells_cell = [x.小区号 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y)for x, y in zip(top_cells_enb, top_cells_cell)]
    return render_template('rrc_rate_list.html', top_cells_info=top_cells_info, top_cells_name=top_cells_name)

@app.route("/rrc_rate_top/<cell_info>", methods=['GET', 'POST'])
def show_rrc_rate_detail(cell_info):
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    weeks = session_rrc.execute("SELECT DISTINCT `周` from `rrc重建`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week =max(weeks)

    qtem_rrc = session_kpi.execute(
        "SELECT tim,rrc FROM (select WEEK(`时间`) as tim,RRC连接重建成功率 AS rrc from kpi_summary where 厂家='不区分厂家' GROUP BY WEEK(`时间`) ORDER BY WEEK(`时间`) DESC LIMIT 5)as a ORDER BY tim ASC")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [str(x.tim) for x in qtem_rrc]
    qtem_rrc_data = [x[1] for x in qtem_rrc]

    recon_rate = session_rrc.execute(
        "SELECT `小区名称`,`日期`,`RRC连接重建成功率`,`RRC重建失败数目` FROM `rrc重建` where 站号 = {enb} and `小区号` ={cell} order by `日期` DESC LIMIT 5 ".format(
            enb=enb, cell=cell))
    recon_rate = list(recon_rate)
    cell_name = recon_rate[0].小区名称
    rate = [x.RRC连接重建成功率 for x in recon_rate]
    fail_count = [x.RRC重建失败数目 for x in recon_rate]
    qw_rrc_chart = draw_line2('RRC重建成功率',qtem_rrc_x_axis, '全网RRC重建成功率', qtem_rrc_data, '本小区RRC重建成功率',rate)
    rrc_fail_count = draw_bar('RRC重建失败数目',fail_count,qtem_rrc_x_axis,' ')

    recon_count = session_rrc.execute(
            "SELECT 站号, `小区号`, `RRC重建请求数目`, `切换类型的RRC重建立失败数目`, `重配置类型的RRC重建立失败数目`, `其它类型的RRC重建立失败数目`,`切换类型的RRC连接重建立成功次数`,`切换类型的RRC重建立失败数目`,`重配置类型的RRC连接重建立成功次数`,`重配置类型的RRC重建立失败数目`,`其它类型的RRC连接重建立成功次数`,`其它类型的RRC重建立失败数目`, `切换类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时`, `切换类型的RRC连接重建立失败次数_失败原因eNB接纳失败`, `切换类型的RRC连接重建立失败次数_失败原因UE上下文找不到`, `切换类型的RRC连接重建立失败次数_失败原因再次重建立`, `切换类型的RRC连接重建立失败次数_其他原因`, `重配置类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时`, `重配置类型的RRC连接重建立失败次数_失败原因eNB接纳失败`, `重配置类型RRC连接重建立失败次数_失败原因UE上下文找不到`, `重配置类型RRC连接重建立失败次数_失败原因再次重建立`, `重配置类型RRC连接重建立失败次数_其他原因`, `其它类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时`, `其它类型的RRC连接重建立失败次数_失败原因eNB接纳失败`, `其它类型的RRC连接重建立失败次数_失败原因UE上下文找不到`, `其它类型的RRC连接重建立失败次数_失败原因再次重建立`, `其它类型的RRC连接重建立失败次数_其他原因` FROM `rrc重建` where 站号 = {enb} and `小区号` ={cell} and `周` = {week}".format(
            enb=enb, cell=cell, week=cur_week))
    recon_rate_pie = list(recon_count)[0]
    recon_count = recon_rate_pie[3:6]
    recon_ho = recon_rate_pie[6:8]
    recon_re = recon_rate_pie[8:10]
    recon_other = recon_rate_pie[10:12]
    recon_ho_cause = recon_rate_pie[12:17]
    recon_re_cause = recon_rate_pie[17:22]
    recon_other_cause = recon_rate_pie[22:]

    recon_count_chart = draw_pie(['切换类型', '重配置类型', '其它类型'], recon_count, 'RRC重建失败原因:', 'RRC重建失败原因')
    recon_ho_chart = draw_pie(['切换类型的RRC连接重建立成功次数', '切换类型的RRC重建立失败数目'], recon_ho, '切换类型的RRC连接重建立次数:', '切换类型的RRC连接重建立次数')
    recon_re_chart = draw_pie(['重配置类型的RRC连接重建立成功次数', '重配置类型的RRC重建立失败数目'], recon_re, '重配置类型的RRC连接重建立次数:', '重配置类型的RRC连接重建立次数')
    recon_other_chart = draw_pie(['其它类型的RRC连接重建立成功次数', '其它类型的RRC重建立失败数目'], recon_other, '其它类型的RRC连接重建立次数:', '其它类型的RRC连接重建立次数')
    recon_ho_cause_chart = draw_pie(['失败原因等待RRC连接重建立完成定时器超时', '失败原因eNB接纳失败', '失败原因UE上下文找不到', '失败原因再次重建立', '其他原因'], recon_ho_cause,'切换类型的RRC连接重建立原因:','切换类型的RRC连接重建立原因')
    recon_re_cause_chart = draw_pie(['失败原因等待RRC连接重建立完成定时器超时', '失败原因eNB接纳失败', '失败原因UE上下文找不到','失败原因再次重建立', '其他原因'], recon_re_cause, '重配置类型的RRC连接重建立原因:','重配置类型的RRC连接重建立原因')
    recon_other_cause_chart = draw_pie(['失败原因等待RRC连接重建立完成定时器超时', '失败原因eNB接纳失败', '失败原因UE上下文找不到','失败原因再次重建立', '其他原因'], recon_other_cause, '其它类型的RRC连接重建立原因:','其它类型的RRC连接重建立原因')

    return render_template('rrc_rate_detail.html', cell_name=cell_name,
                           qw_rrc_chart_options=qw_rrc_chart.dump_options(), rrc_fail_count_options=rrc_fail_count.dump_options(),
                            recon_count_chart_options=recon_count_chart.dump_options(),recon_ho_chart_options=recon_ho_chart.dump_options(),
                           recon_re_chart_options=recon_re_chart.dump_options(),recon_other_chart_options=recon_other_chart.dump_options(),
                           recon_ho_cause_chart_options=recon_ho_cause_chart.dump_options(),recon_re_cause_chart_options=recon_re_cause_chart.dump_options(),
                           recon_other_cause_chart_options=recon_other_cause_chart.dump_options())

@app.route("/erab")
def show_erab_rate():
    qtem_rrc = session_kpi.execute(
        "select 时间,E_RAB掉线率 from(select 时间,E_RAB掉线率 from kpi_summary where 厂家='不区分厂家' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [x.时间 for x in qtem_rrc]
    qtem_rrc_data = [x.E_RAB掉线率 for x in qtem_rrc]
    qw_rrc = draw_line(qtem_rrc_x_axis, '全网E_RAB掉线率', qtem_rrc_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,E_RAB掉线率 from(select 时间,E_RAB掉线率 from kpi_summary where 厂家='中兴' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [x[1] for x in item_rrc1]
    item_rrc2 = session_kpi.execute(
        "select 时间,E_RAB掉线率 from(select 时间,E_RAB掉线率 from kpi_summary where 厂家='中兴' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc2 = list(item_rrc2)
    item_rrc_n800_data = [x[1] for x in item_rrc2]
    zte_rrc = draw_line2('中兴两网指标对比', item_rrc_x_axis, '中兴800M', item_rrc_800_data, '中兴非800M', item_rrc_n800_data)

    rtem_rrc = session_kpi.execute(
        "select 时间,E_RAB掉线率 from(select 时间,E_RAB掉线率 from kpi_summary where 厂家='爱立信' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data = [x[1] for x in rtem_rrc1]
    rtem_rrc2 = session_kpi.execute(
        "select 时间,E_RAB掉线率 from(select 时间,E_RAB掉线率 from kpi_summary where 厂家='爱立信' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc2 = list(rtem_rrc2)
    rtem_rrc_n800_data = [x[1] for x in rtem_rrc2]
    eri_rrc = draw_line2('爱立信两网指标对比', rtem_rrc_x_axis, '爱立信800M', rtem_rrc_800_data, '爱立信非800M', rtem_rrc_n800_data)

    htem_rrc = session_kpi.execute(
        "select 时间,E_RAB掉线率 from(select 时间,E_RAB掉线率 from kpi_summary where 厂家='华为' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    htem_rrc1 = list(htem_rrc)
    htem_rrc_x_axis = [x[0] for x in htem_rrc1]
    htem_rrc_data = [x[1] for x in htem_rrc1]
    hw_rrcc = draw_line(htem_rrc_x_axis, '华为', htem_rrc_data, '华为', )

    return render_template('rrc_erab_report.html', zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(), qw_rrc_options=qw_rrc.dump_options())

@app.route("/Wireless")
def show_wire_conn():
    qtem_rrc = session_kpi.execute(
        "select 时间,无线连接成功率 from(select 时间,无线连接成功率 from kpi_summary where 厂家='不区分厂家' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [x.时间 for x in qtem_rrc]
    qtem_rrc_data = [x.无线连接成功率 for x in qtem_rrc]
    qw_rrc = draw_line(qtem_rrc_x_axis, '全网无线连接成功率', qtem_rrc_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,无线连接成功率 from(select 时间,无线连接成功率 from kpi_summary where 厂家='中兴' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [x[1] for x in item_rrc1]
    item_rrc2 = session_kpi.execute(
        "select 时间,无线连接成功率 from(select 时间,无线连接成功率 from kpi_summary where 厂家='中兴' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc2 = list(item_rrc2)
    item_rrc_n800_data = [x[1] for x in item_rrc2]
    zte_rrc = draw_line2('中兴两网指标对比', item_rrc_x_axis, '中兴800M', item_rrc_800_data, '中兴非800M', item_rrc_n800_data)

    rtem_rrc = session_kpi.execute(
        "select 时间,无线连接成功率 from(select 时间,无线连接成功率 from kpi_summary where 厂家='爱立信' and 频段标识='800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data = [x[1] for x in rtem_rrc1]
    rtem_rrc2 = session_kpi.execute(
        "select 时间,无线连接成功率 from(select 时间,无线连接成功率 from kpi_summary where 厂家='爱立信' and 频段标识='非800M' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc2 = list(rtem_rrc2)
    rtem_rrc_n800_data = [x[1] for x in rtem_rrc2]
    eri_rrc = draw_line2('爱立信两网指标对比', rtem_rrc_x_axis, '爱立信800M', rtem_rrc_800_data, '爱立信非800M', rtem_rrc_n800_data)

    htem_rrc = session_kpi.execute(
        "select 时间,无线连接成功率 from(select 时间,无线连接成功率 from kpi_summary where 厂家='华为' order by 时间 DESC LIMIT 30)aa ORDER BY 时间 asc")
    session_kpi.close()
    htem_rrc1 = list(htem_rrc)
    htem_rrc_x_axis = [x[0] for x in htem_rrc1]
    htem_rrc_data = [x[1] for x in htem_rrc1]
    hw_rrcc = draw_line(htem_rrc_x_axis, '华为', htem_rrc_data, '华为', )

    return render_template('wire_conn_report.html', zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(), qw_rrc_options=qw_rrc.dump_options())

@app.route("/handover/<cell_info>", methods=['GET', 'POST'])
def show_handover(cell_info):
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    weeks = session_rrc.execute("SELECT DISTINCT week(`日期`) from `rrc重建`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week =max(weeks)

    ho_count = session_handover.execute(
        "SELECT `小区名称`,`邻区`, `切换出请求总次数`,`切换出成功次数`, `切换出失败次数`, `切换出执行失败次数_源侧发生重建立`, `切换出执行失败次数_等待UECONTEXTRELEASE消息超时`, `切换出执行失败次数_其它原因`, `切换出准备失败次数_等待切换响应定时器超时`, `切换出准备失败次数_目标侧准备失败`, `切换出准备失败次数_其它原因`, `切换出准备失败次数_源侧发生重建立`, `切换出准备失败次数_用户未激活`, `切换出准备失败次数_传输资源受限`,`切换入成功次数`, `切换入失败次数`, `切换入执行失败次数_RRC重配完成超时`, `切换入执行失败次数_源侧取消切换`, `切换入执行失败次数_目标侧发生重建立`, `切换入执行失败次数_其他原因`, `切换入准备失败次数_资源分配失败`, `切换入准备失败次数_源侧取消切换`, `切换入准备失败次数_目标侧发生重建立`, `切换入准备失败次数_传输资源受限`, `切换入准备失败次数_其它原因` FROM `邻区切换` WHERE eNodeB = {enb} and `小区` = {cell} and `周`= {week}  and `切换出失败次数`>0  order by 切换出请求总次数 asc limit 40".format(
            enb=enb, cell=cell, week=cur_week))
    ho_count = list(ho_count)
    cell_name = ho_count[0].小区名称
    ho_ne = [x.邻区 for x in ho_count]
    ho_suc_out = [x.切换出成功次数 for x in ho_count]
    ho_fail_out = [x.切换出失败次数 for x in ho_count]
    # ho_outpr_fail_1 = [x.切换出准备失败次数_等待切换响应定时器超时 for x in ho_count]
    # ho_outpr_fail_2 = [x.切换出准备失败次数_目标侧准备失败 for x in ho_count]
    # ho_outpr_fail_3 = [x.切换出准备失败次数_其它原因 for x in ho_count]
    # ho_outpr_fail_4 = [x.切换出准备失败次数_源侧发生重建立 for x in ho_count]
    # ho_outpr_fail_5 = [x.切换出准备失败次数_用户未激活 for x in ho_count]
    # ho_outpr_fail_6 = [x.切换出准备失败次数_传输资源受限 for x in ho_count]
    ho_outdo_fail_1= [x.切换出执行失败次数_源侧发生重建立 for x in ho_count]
    ho_outdo_fail_2 = [x.切换出执行失败次数_等待UECONTEXTRELEASE消息超时 for x in ho_count]
    ho_outdo_fail_3 = [x.切换出执行失败次数_其它原因 for x in ho_count]
    ho_suc_in = [x.切换入成功次数 for x in ho_count]
    ho_fail_in = [x.切换入失败次数 for x in ho_count]
    ho_do_in_1 = [x.切换入执行失败次数_RRC重配完成超时 for x in ho_count]
    ho_do_in_2 = [x.切换入执行失败次数_源侧取消切换 for x in ho_count]
    ho_do_in_3 = [x.切换入执行失败次数_目标侧发生重建立 for x in ho_count]
    ho_do_in_4 = [x.切换入执行失败次数_其他原因 for x in ho_count]
    # ho_pr_in_1 = [x.切换入准备失败次数_资源分配失败 for x in ho_count]
    # ho_pr_in_2 = [x.切换入准备失败次数_源侧取消切换 for x in ho_count]
    # ho_pr_in_3 = [x.切换入准备失败次数_目标侧发生重建立 for x in ho_count]
    # ho_pr_in_4 = [x.切换入准备失败次数_传输资源受限 for x in ho_count]
    # ho_pr_in_5 = [x.切换入准备失败次数_其它原因 for x in ho_count]
    ho_out_cnt_chart = draw_bar_stack(ho_ne,'切换出成功次数',ho_suc_out,'切换出失败次数',ho_fail_out,'切换分析')
    ho_in_cnt_chart = draw_bar_stack(ho_ne, '切换入成功次数', ho_suc_in, '切换入失败次数', ho_fail_in, '切换分析')
    # ho_outpr_fail_chart = draw_bar_stack_6(['' for x in range(len(ho_ne))],'等待切换响应超时',ho_outpr_fail_1,'目标侧准备失败',ho_outpr_fail_2,'其它原因',ho_outpr_fail_3,'源侧发生重建立',ho_outpr_fail_4,'用户未激活',ho_outpr_fail_5,'传输资源受限',ho_outpr_fail_6,'切换出准备失败', )
    ho_outdo_fail_chart = draw_bar_stack_3(['' for x in range(len(ho_ne))],'源侧发生重建立',ho_outdo_fail_1,'UECONTEXTRELEASE超时',ho_outdo_fail_2,'其它原因',ho_outdo_fail_3,'切换出执行失败')
    ho_indo_fail_chart = draw_bar_stack_4(['' for x in range(len(ho_ne))], 'RRC重配完成超时', ho_do_in_1, '源侧取消切换',
                                      ho_do_in_2, '目标侧发生重建立', ho_do_in_3, '其他原因', ho_do_in_4,  '切换入执行失败', )
    # ho_inpr_fail_chart = draw_bar_stack_5(['' for x in range(len(ho_ne))], '资源分配失败', ho_pr_in_1, '源侧取消切换',
    #                                   ho_pr_in_2, '目标侧发生重建立', ho_pr_in_3, '传输资源受限', ho_pr_in_4, '其它原因',
    #                                   ho_pr_in_5, '切换入准备失败', )

    ho_distance = session_handover.execute(
        "SELECT a.`邻区`, b.distance from (SELECT `邻区`,`邻区关系`,`切换出请求总次数` FROM `邻区切换` WHERE eNodeB = {enb} and 小区 = {cell} and `切换出失败次数`>0  order by 切换出请求总次数 asc limit 40) as a left JOIN  (SELECT relation,distance from `邻区距离`) as b ON a.`邻区关系`=b.relation order by a.`切换出请求总次数`".format(enb =enb ,cell = cell))
    ho_distance = list(ho_distance)
    distance_ce = [x.邻区 for x in ho_distance]
    df_distance = [x.distance for x in ho_distance]
    ho_distance_chart = draw_bar_reversal(['' for x in range(len(distance_ce))], df_distance, '邻区站点距离', ' ', )

    session_rrc.close()
    session_handover.close()
    
    return render_template('hand_over.html',
                           cell_name=cell_name,
                           ho_out_cnt_chart_options=ho_out_cnt_chart.dump_options(),
                           ho_distance_chart_options=ho_distance_chart.dump_options(),
                           ho_mod3_chart_options=ho_distance_chart.dump_options(),
                           )


@app.route('/put', methods=['GET', 'POST'])
def put2datebase():
    # 将表单类实例化
    form = Complaint_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            complaint_info = request.form.to_dict()
            item = session_tousu.execute('select * from tousu order by 工单流水号 asc')
            session_tousu.close()
            item = list(item)
            item = str([x[0] for x in item])
            # conutry,town = get_country_town(complaint_info)
            if complaint_info['serial_number'] not in item:
                put2base(complaint_info, session_tousu)
            else:
                updata2base(complaint_info, session_tousu)
            return render_template('put_succ.html', complaint_info=complaint_info)
    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run()
