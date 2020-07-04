# -*- coding: utf-8 -*-

from flask import Flask, url_for, request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tousu
from forms import Complaint_form, Select_form,Rrc_recon_form,Rrc_rate_form,Erab_drop_form,Vol_connect_form,Vol_drop_form
from config import Config
from func import draw_bar, draw_line3, draw_line2, draw_line, draw_pie, draw_bar_reversal, draw_bar2_reversal, draw_bar_stack_3, draw_bar_stack, draw_bar_stack_6, draw_bar_stack_4, draw_bar_stack_5,draw_bar2,updata_rrc_reconn,updata_rrc_rate,updata_erab_drop,updata_vol_connect,updata_vol_drop
import datetime
import time

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.config.from_object(Config)

engine_mr = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/mr_report?charset=utf8", pool_recycle=7200)
engine_cqi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/cqi_report?charset=utf8", pool_recycle=7200)
engine_tousu = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/qjwx_tousu?charset=utf8",
                             pool_recycle=7200)
engine_kpi = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/kpi_report?charset=utf8", pool_recycle=7200)
engine_rrc = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/rrc_reconnect?charset=utf8",
                           pool_recycle=7200)
engine_handover = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/hand_over?charset=utf8",
                           pool_recycle=7200)
engine_erab= create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/e_rab?charset=utf8",
                           pool_recycle=7200)
engine_vol= create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/volte?charset=utf8",
                           pool_recycle=7200)

Session_mr = sessionmaker(autocommit=False, autoflush=True, bind=engine_mr)
Session_cqi = sessionmaker(autocommit=False, autoflush=True, bind=engine_cqi)
Session_tousu = sessionmaker(autocommit=False, autoflush=True, bind=engine_tousu)
Session_kpi = sessionmaker(autocommit=False, autoflush=True, bind=engine_kpi)
Session_rrc = sessionmaker(autocommit=False, autoflush=True, bind=engine_rrc)
Session_handover = sessionmaker(autocommit=False, autoflush=True, bind=engine_handover)
Session_erab = sessionmaker(autocommit=False, autoflush=True, bind=engine_erab)
Session_vol = sessionmaker(autocommit=False, autoflush=True, bind=engine_vol)

session_mr = Session_mr()
session_cqi = Session_cqi()
session_tousu = Session_tousu()
session_kpi = Session_kpi()
session_rrc = Session_rrc()
session_handover = Session_handover()
session_erab = Session_erab()
session_vol = Session_vol()


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


@app.route("/traffic", methods=['GET', 'POST'])
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
    cur_week = session_rrc.execute("SELECT max(`周`) from `rrc重建比例top小区`")
    cur_week = list(cur_week)[0][0]

    top_cells = session_rrc.execute(
        "SELECT * from `rrc重建比例top小区` WHERE  `周`= {cur_week} LIMIT 20".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.站号 for x in top_cells]
    top_cells_cell = [x.小区号 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    recon_count = [x.RRC重建请求数目 for x in top_cells]
    recon_rate = [x.RRC重建立比例 for x in top_cells]
    res = [x.重建原因 for x in top_cells]
    mea = [x.处理措施 for x in top_cells]
    hand = [x.处理人 for x in top_cells]
    session_rrc.close()

    table_titles = ['小区名称', 'RRC重建请求数目', 'RRC重建立比例', '重建原因', '处理措施','处理人']
    return render_template('rrc_recon_list.html', table_titles=table_titles,top_cells_info=top_cells_info, top_cells_name=top_cells_name,
                           recon_count=recon_count, recon_rate=recon_rate, res=res,mea=mea,hand=hand)

@app.route("/rrc_recon_top/<cell_info>", methods=['GET', 'POST'])
def show_rrc_recon_detail(cell_info):
    form = Rrc_recon_form()
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    cur_week = session_rrc.execute("SELECT max(`周`) from `rrc重建比例top小区`")
    cur_week = list(cur_week)[0][0]
    now_time = datetime.datetime.now()
    now_time = int(str(now_time).split(' ')[0].split('-')[1])
    recon_ratio = session_rrc.execute(
        "SELECT 周, `小区号`, `RRC重建立比例`, `RRC重建请求数目`, `RRC连接重建成功率`,`小区名称` FROM (SELECT 周,站号, `小区号`, `RRC重建立比例`, `RRC重建请求数目`, `RRC连接重建成功率`,`小区名称` FROM `rrc重建比例top小区` where 站号 = {enb} and `小区号` ={cell} order by 周 DESC LIMIT 4) a ORDER BY 周 LIMIT 4".format(
            enb=enb, cell=cell))
    recon_ratio = list(recon_ratio)
    cell_name = [x[5] for x in recon_ratio][0]
    datax = [str(x[0]) for x in recon_ratio]
    ratio =  [x[2] for x in recon_ratio]
    ratio_sec= [x[4] for x in recon_ratio]
    recon_count = [x[3] for x in recon_ratio]
    recon_ratio_chart = draw_line2(' ',datax,'RRC重建比例', ratio, 'RRC连接重建成功率',ratio_sec)
    recon_count_chart = draw_bar('RRC重建请求次数', recon_count,  datax, 'RRC重建次数')

    recon_reason = session_rrc.execute(
        "SELECT 站号, `小区号`, `RRC重建请求数目`, `切换失败触发的RRC重建立请求次数`, `其它原因触发的RRC重建立请求次数`, `重配失败触发的RRC重建立请求次数` FROM `rrc重建比例top小区` where 站号 = {enb} and `小区号` ={cell} and 周 = {week}".format(
            enb=enb, cell=cell, week=cur_week))
    recon_reason = list(recon_reason)[0]
    recon_reason = recon_reason[3:]
    recon_reason_chart = draw_pie(['切换失败','其它原因','重配失败'],recon_reason,'RRC重建原因:','RRC重建原因')

    item_TA = session_kpi.execute(
        "select TA0_1,TA1_3,TA3_5,TA5_7,TA7_9,TA9_11,TA11_13,TA13_20,TA20_27,TA27_34,TA34_40,TA40_50,TA50_81,TA81_129,TA129_179 FROM zte_day_{}  where 站号 = {} and 小区号 = {} ORDER BY 日期 DESC LIMIT 1".format(
            6,enb, cell))
    session_kpi.close()
    item_TA = list(item_TA)
    item_TA = list(item_TA[0])
    item_TA_x_axis = ['78.12m', '78~234m', '234~390m', '390~547m', '547~703m', '703~859m', '859~1015m', '1015~1562m',
                      '1562~2109m', '2109~2656m', '2656~3125m', '3125~3906m', '3906~6328m', '6328~10077m', '10077~13983m']
    item_TA_y_data = item_TA
    TA_dist_chart = draw_bar('TA分布',item_TA_y_data,item_TA_x_axis,'TA分布')

    item_MR = session_mr.execute(
        "select above105,between110and105,between115and110,between120and115 FROM mr_rrc_reconn_top where top_time = {} and enb={} and cell={} ORDER BY top_time DESC LIMIT 1".format(
            cur_week,enb, cell))
    session_mr.close()
    item_MR = list(item_MR)
    item_MR = list(item_MR[0])
    item_MR_x_axis = ['优于-105dBm', '-105dBm~-110dBm', '-110dBm~-115dBm', '-115dBm~-120dBm']
    item_MR_y_data = item_MR
    MR_dist_chart = draw_bar('MR分布', item_MR_y_data, item_MR_x_axis, 'MR分布')

    rrc_rec = session_kpi.execute(
        "select 日期,系统内切换成功率 from(select 日期,系统内切换成功率 from zte_day_{} where 站号 = {} and 小区号 = {} order by 日期 DESC LIMIT 10)aa ORDER BY 日期 asc".format(
            6,enb, cell))
    session_kpi.close()
    rrc_rec = list(rrc_rec)
    rrc_rec_x_axis = [x[0] for x in rrc_rec]
    rec_ho_y_data = [round(x[1] * 100, 2) for x in rrc_rec]
    recon_kpi_chart = draw_line(rrc_rec_x_axis, ' ', rec_ho_y_data,'系统内切换成功率' )

    if request.method == 'POST':
        if form.validate_on_submit():
            complaint_info = request.form.to_dict()
            eNodbe_num = cell_name.split('_')[0]
            eNodbe_cell = cell_name.split('_')[1]
            complaint_info.update({'eNodbe_name':cell_name,'eNodbe_number':eNodbe_num,'eNodbe_cell':eNodbe_cell})

            updata_rrc_reconn(complaint_info, session_rrc)
            return render_template('put_rrc_recon_succ.html',
                                   complaint_info=complaint_info)

    return render_template('rrc_recon_detail.html', cell_name = cell_name,rrc_recon_reason_chart_options=recon_reason_chart.dump_options(),
                           rrc_recon_ratio_chart_options=recon_ratio_chart.dump_options(),rrc_recon_count_chart_options=recon_count_chart.dump_options(),
                           TA_dist_chart_options=TA_dist_chart.dump_options(),MR_dist_chart_options=MR_dist_chart.dump_options(),recon_kpi_chart_options=recon_kpi_chart.dump_options(),form=form)



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
    cur_week = session_rrc.execute("SELECT max(`周`) from `rrc重建成功率top小区`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_rrc.execute(
        "SELECT * from `rrc重建成功率top小区` WHERE  `周`= {cur_week} ".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.站号 for x in top_cells]
    top_cells_cell = [x.小区号 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    recon_count = [x.RRC重建失败数目 for x in top_cells]
    recon_rate = [x.RRC连接重建成功率 for x in top_cells]
    res = [x.重建原因 for x in top_cells]
    mea = [x.处理措施 for x in top_cells]
    hand = [x.处理人 for x in top_cells]
    session_rrc.close()

    table_titles = ['小区名称', 'RRC重建失败数目', 'RRC连接重建成功率', '重建原因', '处理措施', '处理人']
    return render_template('rrc_rate_list.html', table_titles=table_titles, top_cells_info=top_cells_info,
                           top_cells_name=top_cells_name,
                           recon_count=recon_count, recon_rate=recon_rate, res=res, mea=mea, hand=hand)

@app.route("/rrc_rate_top/<cell_info>", methods=['GET', 'POST'])
def show_rrc_rate_detail(cell_info):
    form = Rrc_rate_form()
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    cell_name =  session_rrc.execute("SELECT `小区名称` FROM `rrc重建` where `站号` = {enb} and `小区号` = {cell}".format(enb=enb, cell=cell))
    cell_name = list(cell_name)
    cell_name = cell_name[0].小区名称
    weeks = session_rrc.execute("SELECT DISTINCT week(`日期`) from `rrc重建`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week = session_rrc.execute("SELECT max(week(`日期`)) from `rrc重建`")
    cur_week = list(cur_week)[0][0]

    qtem_rrc = session_kpi.execute(
        "SELECT tim,rrc FROM (select WEEK(`时间`) as tim,RRC连接重建成功率 AS rrc from kpi_summary where 厂家='不区分厂家' GROUP BY WEEK(`时间`) ORDER BY WEEK(`时间`) DESC LIMIT 5)as a ORDER BY tim ASC")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [str(x.tim) for x in qtem_rrc]
    qtem_rrc_data = [x[1] for x in qtem_rrc]

    recon_rate = session_rrc.execute(
        "SELECT `日期`,`RRC连接重建成功率`,`RRC重建失败数目` FROM `rrc重建` where 站号 = {enb} and `小区号` ={cell} order by `日期` DESC LIMIT 5 ".format(
            enb=enb, cell=cell))
    recon_rate = list(recon_rate)
    rate = [x[1] for x in recon_rate]
    fail_count = [x[2] for x in recon_rate]
    qw_rrc_chart = draw_line2('RRC重建成功率',qtem_rrc_x_axis, '全网RRC重建成功率', qtem_rrc_data, '本小区RRC重建成功率',rate)
    rrc_fail_count = draw_bar('RRC重建失败数目',fail_count,qtem_rrc_x_axis,' ')

    recon_count = session_rrc.execute(
            "SELECT 站号, `小区号`, `RRC重建请求数目`, `切换类型的RRC重建立失败数目`, `重配置类型的RRC重建立失败数目`, `其它类型的RRC重建立失败数目`,`切换类型的RRC连接重建立成功次数`,`切换类型的RRC重建立失败数目`,`重配置类型的RRC连接重建立成功次数`,`重配置类型的RRC重建立失败数目`,`其它类型的RRC连接重建立成功次数`,`其它类型的RRC重建立失败数目`, `切换类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时`, `切换类型的RRC连接重建立失败次数_失败原因eNB接纳失败`, `切换类型的RRC连接重建立失败次数_失败原因UE上下文找不到`, `切换类型的RRC连接重建立失败次数_失败原因再次重建立`, `切换类型的RRC连接重建立失败次数_其他原因`, `重配置类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时`, `重配置类型的RRC连接重建立失败次数_失败原因eNB接纳失败`, `重配置类型RRC连接重建立失败次数_失败原因UE上下文找不到`, `重配置类型RRC连接重建立失败次数_失败原因再次重建立`, `重配置类型RRC连接重建立失败次数_其他原因`, `其它类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时`, `其它类型的RRC连接重建立失败次数_失败原因eNB接纳失败`, `其它类型的RRC连接重建立失败次数_失败原因UE上下文找不到`, `其它类型的RRC连接重建立失败次数_失败原因再次重建立`, `其它类型的RRC连接重建立失败次数_其他原因` FROM `rrc重建` where 站号 = {enb} and `小区号` ={cell} and week(`日期`) = {week}".format(
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

    if request.method == 'POST':
        if form.validate_on_submit():
            complaint_info = request.form.to_dict()
            now_time = time.ctime(time.time())
            now_time = now_time.split(' ')[1] + now_time.split(' ')[2]
            eNodbe_num = cell_name.split('_')[0] + '_' + cell_name.split('_')[1] + '_' + now_time
            complaint_info.update({'eNodbe_name':cell_name,'eNodbe_number':eNodbe_num})
            item = session_rrc.execute('select * from rrc_rate')
            session_rrc.close()
            item = list(item)
            item = str([x[0] for x in item])
            if complaint_info['eNodbe_number'] not in item:
                rrc_rate_put(complaint_info,session_rrc)
            else:
                updata_rrc_rate(complaint_info, session_rrc)
            return render_template('put_rrc_rate_succ.html',
                                   complaint_info=complaint_info)

    return render_template('rrc_rate_detail.html', cell_name=cell_name,
                           qw_rrc_chart_options=qw_rrc_chart.dump_options(), rrc_fail_count_options=rrc_fail_count.dump_options(),
                            recon_count_chart_options=recon_count_chart.dump_options(),recon_ho_chart_options=recon_ho_chart.dump_options(),
                           recon_re_chart_options=recon_re_chart.dump_options(),recon_other_chart_options=recon_other_chart.dump_options(),
                           recon_ho_cause_chart_options=recon_ho_cause_chart.dump_options(),recon_re_cause_chart_options=recon_re_cause_chart.dump_options(),
                           recon_other_cause_chart_options=recon_other_cause_chart.dump_options(),form=form)


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

@app.route("/erab_drop_top/", methods=['GET', 'POST'])
def show_erab_drop_list():
    cur_week = session_erab.execute("SELECT max(`周`) from `e_rab掉线率top小区`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_erab.execute(
        "SELECT * from `e_rab掉线率top小区` WHERE  `周`= {cur_week} ".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.站号 for x in top_cells]
    top_cells_cell = [x.小区号 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    recon_count = [x.E_RAB掉线总次数 for x in top_cells]
    recon_rate = [x.E_RAB掉线率 for x in top_cells]
    res = [x.掉线原因 for x in top_cells]
    mea = [x.处理措施 for x in top_cells]
    hand = [x.处理人 for x in top_cells]
    session_erab.close()

    table_titles = ['小区名称', 'E_RAB掉线总次数', 'E_RAB掉线率', '掉线原因', '处理措施', '处理人']
    return render_template('erab_drop_list.html', table_titles=table_titles, top_cells_info=top_cells_info,
                           top_cells_name=top_cells_name,
                           recon_count=recon_count, recon_rate=recon_rate, res=res, mea=mea, hand=hand)

@app.route("/erab_drop_top/<cell_info>", methods=['GET', 'POST'])
def show_erab_drop_detail(cell_info):
    form = Erab_drop_form()
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    cell_name =  session_erab.execute("SELECT `小区名称` FROM `erab_week` where `站号` = {enb} and `小区号` = {cell}".format(enb=enb, cell=cell))
    cell_name = list(cell_name)
    cell_name = cell_name[0].小区名称
    weeks = session_erab.execute("SELECT DISTINCT 周 from `erab_week`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week = session_erab.execute("SELECT max(周) from `erab_week`")
    cur_week = list(cur_week)[0][0]

    qtem_rrc = session_kpi.execute(
        "SELECT tim,rrc FROM (select WEEK(`时间`) as tim,E_RAB掉线率 AS rrc from kpi_summary where 厂家='不区分厂家' GROUP BY WEEK(`时间`) ORDER BY WEEK(`时间`) DESC LIMIT 5)as a ORDER BY tim ASC")
    session_kpi.close()
    qtem_rrc = list(qtem_rrc)
    qtem_rrc_x_axis = [str(x.tim) for x in qtem_rrc]
    qtem_rrc_data = [x[1] for x in qtem_rrc]

    recon_rate = session_erab.execute(
        "SELECT `日期`,`E_RAB掉线率`,`E_RAB掉线总次数` FROM `erab_week` where 站号 = {enb} and `小区号` ={cell} and 周 = {cur_week} order by `日期` DESC LIMIT 5 ".format(
            enb=enb, cell=cell,cur_week=cur_week))
    recon_rate = list(recon_rate)
    rate = [x[1] for x in recon_rate]
    fail_count = [x[2] for x in recon_rate]
    qw_rrc_chart = draw_line2('E_RAB掉线率',weeks, '全网E_RAB掉线率', qtem_rrc_data, '本小区E_RAB掉线率',rate)
    rrc_fail_count = draw_bar('E_RAB掉线总次数',fail_count,weeks,' ')

    recon_count = session_erab.execute(
            "SELECT 站号, `小区号`, `E_RAB释放次数_由于ENB过载控制导致的释放`, `E_RAB释放次数_由于ENB其他异常原因`, `E_RAB释放次数_由于ENB小区拥塞导致的释放`, `E_RAB释放次数_由于ENB的无线链路失败`,`E_RAB释放次数_由于ENB重建立失败`,`E_RAB释放次数_由于小区关断或复位`,`E_RAB释放次数_跨站重建立失败导致的释放`,`E_RAB释放次数_ENB由于S1链路故障发起释放`,`E_RAB释放次数_由于UE不在线导致释放` FROM `erab_week` where 站号 = {enb} and `小区号` ={cell}".format(
            enb=enb, cell=cell))
    recon_rate_pie = list(recon_count)[0]
    recon_count = recon_rate_pie[2:]

    recon_count_chart = draw_pie(['E_RAB释放次数_由于ENB过载控制导致的释放', 'E_RAB释放次数_由于ENB其他异常原因', 'E_RAB释放次数_由于ENB小区拥塞导致的释放', 'E_RAB释放次数_由于ENB的无线链路失败', 'E_RAB释放次数_由于ENB重建立失败', 'E_RAB释放次数_由于小区关断或复位', 'E_RAB释放次数_跨站重建立失败导致的释放', 'E_RAB释放次数_ENB由于S1链路故障发起释放', 'E_RAB释放次数_由于UE不在线导致释放'], recon_count, 'E_RAB掉线原因:', 'E_RAB掉线原因')

    if request.method == 'POST':
        if form.validate_on_submit():
            complaint_info = request.form.to_dict()
            now_time = time.ctime(time.time())
            now_time = now_time.split(' ')[1] + now_time.split(' ')[2]
            eNodbe_num = cell_name.split('_')[0] + '_' + cell_name.split('_')[1] + '_' + now_time
            complaint_info.update({'eNodbe_name':cell_name,'eNodbe_number':eNodbe_num})
            item = session_erab.execute('select * from erab_drop')
            session_erab.close()
            item = list(item)
            item = str([x[0] for x in item])
            if complaint_info['eNodbe_number'] not in item:
                erab_drop_put(complaint_info,session_erab)
            else:
                updata_erab_drop(complaint_info, session_erab)
            return render_template('put_erab_succ.html',
                                   complaint_info=complaint_info)
    return render_template('erab_drop_detail.html', cell_name=cell_name,
                           qw_rrc_chart_options=qw_rrc_chart.dump_options(), rrc_fail_count_options=rrc_fail_count.dump_options(),
                            recon_count_chart_options=recon_count_chart.dump_options(),form=form)

@app.route("/volte rate")
def show_volte_rate():
    cur_day = session_vol.execute("SELECT max(DAY(日期)) from `vol_rate`")
    cur_day = list(cur_day)[0][0]
    vtem_vol = session_vol.execute(
        "select 日期,下行QCI_1最大激活用户数,下行QCI_2最大激活用户数,E_RAB建立请求数目_QCI_1,E_RAB建立请求数目_QCI_2 from vol_rate where DAY(日期)={cur_day}".format(cur_day=cur_day))
    session_kpi.close()
    vtem_vol = list(vtem_vol)
    vtem_vol_x_axis = [str(x.日期).split(' ')[1] for x in vtem_vol]
    vtem_vol_data1 = [x.下行QCI_1最大激活用户数 for x in vtem_vol]
    vtem_vol_data2 = [x.下行QCI_2最大激活用户数 for x in vtem_vol]
    vtem_vol_requ1 = [x.E_RAB建立请求数目_QCI_1 for x in vtem_vol]
    vtem_vol_requ2 = [x.E_RAB建立请求数目_QCI_2 for x in vtem_vol]
    vol_user = draw_bar2('全网Volte语音用户数','全网Volte视频用户数', vtem_vol_data1,vtem_vol_data2, vtem_vol_x_axis,
                         '全市{cur_day}日Volte用户数'.format(cur_day=cur_day))
    vol_request = draw_bar2('全网Volte语音呼叫次数', '全网Volte视频呼叫次数', vtem_vol_requ1, vtem_vol_requ2, vtem_vol_x_axis,
                            '全市{cur_day}日Volte呼叫次数'.format(cur_day=cur_day))

    qtem_vol = session_kpi.execute(
        "select 时间,VoLTE语音无线接通率 from(select 时间,VoLTE语音无线接通率 from kpi_summary_vol_nb where 厂家='不区分厂家' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_vol = list(qtem_vol)
    qtem_vol_x_axis = [x.时间 for x in qtem_vol]
    qtem_vol_data = [x.VoLTE语音无线接通率 for x in qtem_vol]
    qw_rrc = draw_line(qtem_vol_x_axis, '全网VoLTE语音无线接通率', qtem_vol_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,VoLTE语音无线接通率 from(select 时间,VoLTE语音无线接通率 from kpi_summary_vol_nb where 厂家='中兴' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [x[1] for x in item_rrc1]
    zte_rrc = draw_line( item_rrc_x_axis, '中兴', item_rrc_800_data, '中兴')

    rtem_rrc = session_kpi.execute(
        "select 时间,VoLTE语音无线接通率 from(select 时间,VoLTE语音无线接通率 from kpi_summary_vol_nb where 厂家='爱立信' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data = [x[1] for x in rtem_rrc1]
    eri_rrc = draw_line( rtem_rrc_x_axis, '爱立信', rtem_rrc_800_data, '爱立信')

    htem_rrc = session_kpi.execute(
        "select 时间,VoLTE语音无线接通率 from(select 时间,VoLTE语音无线接通率 from kpi_summary_vol_nb where 厂家='华为' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    htem_rrc1 = list(htem_rrc)
    htem_rrc_x_axis = [x[0] for x in htem_rrc1]
    htem_rrc_data = [x[1] for x in htem_rrc1]
    hw_rrcc = draw_line(htem_rrc_x_axis, '华为', htem_rrc_data, '华为', )

    return render_template('vol_rate_report.html', zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(), qw_rrc_options=qw_rrc.dump_options(),
                           vol_user_options=vol_user.dump_options(),vol_request_options=vol_request.dump_options(),)

@app.route("/vol_connect_top/", methods=['GET', 'POST'])
def show_vol_rate_list():
    cur_week = session_vol.execute("SELECT max(`周`) from `vol_rate_top`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_vol.execute(
        "SELECT * from `vol_rate_top` WHERE  `周`= {cur_week} ".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.站号 for x in top_cells]
    top_cells_cell = [x.小区 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    recon_count = [x.小区E_RAB建立成功率_QCI_1 for x in top_cells]
    recon_rate = [x.失败总次数 for x in top_cells]
    res = [x.未接通原因 for x in top_cells]
    mea = [x.处理措施 for x in top_cells]
    hand = [x.处理人 for x in top_cells]
    session_vol.close()

    table_titles = ['小区名称', '接通率', '未接通次数', '未接通原因', '处理措施', '处理人']
    return render_template('vol_rate_top_list.html', table_titles=table_titles, top_cells_info=top_cells_info,
                           top_cells_name=top_cells_name,
                           recon_count=recon_count, recon_rate=recon_rate, res=res, mea=mea, hand=hand)

@app.route("/vol_connect_top/<cell_info>", methods=['GET', 'POST'])
def show_vol_connect_detail(cell_info):
    form = Vol_connect_form()
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    cell_name =  session_vol.execute("SELECT `小区名称` FROM `vol_rate_top` where `网元` = {enb} and `小区` = {cell}".format(enb=enb, cell=cell))
    cell_name = list(cell_name)
    cell_name = cell_name[0].小区名称

    recon_rate = session_vol.execute(
        "SELECT `开始时间`,`小区E_RAB建立成功率_QCI_1`,`失败总次数` FROM `vol_rate_top` where 网元 = {enb} and `小区` = {cell} order by `开始时间` DESC LIMIT 5".format(
            enb=enb, cell=cell))
    recon_rate = list(recon_rate)
    rate = [str(x[0]).split(' ')[0] for x in recon_rate]
    fail_count = [x[2] for x in recon_rate]
    rrc_fail_count = draw_bar('Volte未接通总次数',fail_count,rate,' ')

    recon_count = session_vol.execute(
            "SELECT 网元, `小区`, `QCI1_初始的E_RAB建立失败次数_空口失败`, `QCI1_初始的E_RAB建立失败次数_eNB接纳失败`, `QCI1_初始的E_RAB建立失败次数_RRC重建立原因`, `QCI1_初始的E_RAB建立失败次数_传输层原因`,`QCI1_初始的E_RAB建立失败次数_消息参数错误`,`QCI1_初始的E_RAB建立失败次数_安全激活失败`,`QCI1_初始的E_RAB建立失败次数_其他原因`,`QCI1_增加的E_RAB建立失败次数_空口失败`,`QCI1_增加的E_RAB建立失败次数_切换引起`,`QCI1_增加的E_RAB建立失败次数_eNB接纳失败`,`QCI1_增加的E_RAB建立失败次数_RRC重建立原因`,`QCI1_增加的E_RAB建立失败次数_传输层原因`,`QCI1_增加的E_RAB建立失败次数_消息参数错误`,`QCI1_增加的E_RAB建立失败次数_其他原因`,`空口问题占比`,`切换问题占比`,`拥塞占比`,`传输故障占比`,`参数或软件故障占比`,`安全激活失败`,`其他原因占比` FROM `vol_rate_top` where 网元 = {enb} and `小区` ={cell}".format(
            enb=enb, cell=cell))
    recon_rate_pie = list(recon_count)[0]
    recon_count = recon_rate_pie[2:16]
    recon_ratio = recon_rate_pie[16:]

    recon_count_chart = draw_pie(['QCI1_初始的E_RAB建立失败次数_空口失败', 'QCI1_初始的E_RAB建立失败次数_eNB接纳失败', 'QCI1_初始的E_RAB建立失败次数_RRC重建立原因', 'QCI1_初始的E_RAB建立失败次数_传输层原因', 'QCI1_初始的E_RAB建立失败次数_消息参数错误', 'QCI1_初始的E_RAB建立失败次数_安全激活失败', 'QCI1_初始的E_RAB建立失败次数_其他原因', 'QCI1_增加的E_RAB建立失败次数_空口失败', 'QCI1_增加的E_RAB建立失败次数_切换引起', 'QCI1_增加的E_RAB建立失败次数_eNB接纳失败', 'QCI1_增加的E_RAB建立失败次数_RRC重建立原因', 'QCI1_增加的E_RAB建立失败次数_传输层原因', 'QCI1_增加的E_RAB建立失败次数_消息参数错误', 'QCI1_增加的E_RAB建立失败次数_其他原因'], recon_count, 'Volte未接通详细原因:', 'Volte未接通详细原因')
    recon_ratio_chart = draw_pie(['空口问题占比','切换问题占比','拥塞占比','传输故障占比','参数或软件故障占比','安全激活失败','其他原因占比'], recon_ratio, 'Volte未接通原因分类:', 'Volte未接通原因分类')

    if request.method == 'POST':
        if form.validate_on_submit():
            complaint_info = request.form.to_dict()
            now_time = time.ctime(time.time())
            now_time = now_time.split(' ')[1] + now_time.split(' ')[2]
            eNodbe_num = cell_name.split('_')[0] + '_' + cell_name.split('_')[1] + '_' + now_time
            complaint_info.update({'eNodbe_name': cell_name, 'eNodbe_number': eNodbe_num})
            item = session_vol.execute('select * from vol_connect')
            session_vol.close()
            item = list(item)
            item = str([x[0] for x in item])
            if complaint_info['eNodbe_number'] not in item:
                vol_connect_put(complaint_info, session_vol)
            else:
                updata_vol_connect(complaint_info, session_vol)
            return render_template('put_vol_connect_succ.html',
                                   complaint_info=complaint_info)
    return render_template('vol_connect_detail.html', cell_name=cell_name, rrc_fail_count_options=rrc_fail_count.dump_options(),
                            recon_count_chart_options=recon_count_chart.dump_options(),recon_ratio_chart_options=recon_ratio_chart.dump_options(),form=form)


@app.route("/vol_drop_top/", methods=['GET', 'POST'])
def show_vol_drop_list():
    cur_week = session_vol.execute("SELECT max(`周`) from `vol_drop_top`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_vol.execute(
        "SELECT * from `vol_drop_top` WHERE  `周`= {cur_week} ".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.网元 for x in top_cells]
    top_cells_cell = [x.小区 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    recon_count = [x.掉话率 for x in top_cells]
    recon_rate = [x.掉话总次数 for x in top_cells]
    res = [x.掉话原因 for x in top_cells]
    mea = [x.处理措施 for x in top_cells]
    hand = [x.处理人 for x in top_cells]
    session_vol.close()

    table_titles = ['小区名称', '接通率', '未接通次数', '未接通原因', '处理措施', '处理人']
    return render_template('vol_rate_top_list.html', table_titles=table_titles, top_cells_info=top_cells_info,
                           top_cells_name=top_cells_name,
                           recon_count=recon_count, recon_rate=recon_rate, res=res, mea=mea, hand=hand)

@app.route("/vol_drop_top/<cell_info>", methods=['GET', 'POST'])
def show_vol_drop_detail(cell_info):
    form = Vol_drop_form()
    enb = str(cell_info.split('_')[0])
    cell = str(cell_info.split('_')[1])
    cell_name =  session_vol.execute("SELECT `小区名称` FROM `vol_drop_top` where `网元` = {enb} and `小区` = {cell}".format(enb=enb, cell=cell))
    cell_name = list(cell_name)
    cell_name = cell_name[0].小区名称


    recon_rate = session_vol.execute(
        "SELECT a.周,a.drop_sum FROM (SELECT `周`,`掉话总次数` as drop_sum FROM vol_drop_top WHERE 网元 = {enb} and `小区`={cell} ORDER BY 周 DESC LIMIT 5) as a ORDER BY 周 ".format(
            enb=enb, cell=cell))
    recon_rate = list(recon_rate)
    rate = [str(x[0]).split(' ')[0] for x in recon_rate]
    fail_count = [x[1] for x in recon_rate]
    rrc_fail_count = draw_bar('Volte掉话总次数',fail_count,rate,' ')

    recon_count = session_vol.execute(
            "SELECT 网元, `小区`, `QCI1_E_RAB释放次数_由于ENB小区拥塞导致的释放`, `QCI1_E_RAB释放次数_由于ENB过载控制导致的释放`, `QCI1_E_RAB释放次数_由于ENB的无线链路失败`, `QCI1_E_RAB释放次数_由于ENB重建立失败`,`QCI1_E_RAB释放次数_由于小区关断或复位`,`QCI1_E_RAB释放次数_跨站重建立失败导致的释放`,`QCI1_E_RAB释放次数_ENB由于S1链路故障发起释放`,`QCI1_E_RAB释放次数_由于ENB其他异常原因`,`小区拥塞占比`,`无线环境问题占比`,`切换失败占比`,`基站关断或复位占比`,`传输故障占比`,`其他原因占比` FROM `vol_drop_top` where 网元 = {enb} and `小区` ={cell}".format(
            enb=enb, cell=cell))
    recon_rate_pie = list(recon_count)[0]
    recon_count = recon_rate_pie[2:10]
    recon_ratio = recon_rate_pie[10:]

    recon_count_chart = draw_pie(['QCI1_E_RAB释放次数_由于ENB小区拥塞导致的释放', 'QCI1_E_RAB释放次数_由于ENB过载控制导致的释放', 'QCI1_E_RAB释放次数_由于ENB的无线链路失败', 'QCI1_E_RAB释放次数_由于ENB重建立失败', 'QCI1_E_RAB释放次数_由于小区关断或复位', 'QCI1_E_RAB释放次数_跨站重建立失败导致的释放', 'QCI1_E_RAB释放次数_ENB由于S1链路故障发起释放', 'QCI1_E_RAB释放次数_由于ENB其他异常原因', 'QCI1_增加的E_RAB建立失败次数_切换引起', 'QCI1_增加的E_RAB建立失败次数_eNB接纳失败', 'QCI1_增加的E_RAB建立失败次数_RRC重建立原因', 'QCI1_增加的E_RAB建立失败次数_传输层原因', 'QCI1_增加的E_RAB建立失败次数_消息参数错误', 'QCI1_增加的E_RAB建立失败次数_其他原因'], recon_count, 'Volte掉话详细原因:', 'Volte掉话详细原因')
    recon_ratio_chart = draw_pie(['小区拥塞占比','无线环境问题占比','切换失败占比','基站关断或复位占比','传输故障占比','其他原因占比'], recon_ratio, 'Volte掉话原因分类:', 'Volte掉话原因分类')

    if request.method == 'POST':
        if form.validate_on_submit():
            complaint_info = request.form.to_dict()
            now_time = time.ctime(time.time())
            now_time = now_time.split(' ')[1] + now_time.split(' ')[2]
            eNodbe_num = cell_name.split('_')[0] + '_' + cell_name.split('_')[1] + '_' + now_time
            complaint_info.update({'eNodbe_name': cell_name, 'eNodbe_number': eNodbe_num})
            item = session_vol.execute('select * from vol_drop')
            session_vol.close()
            item = list(item)
            item = str([x[0] for x in item])
            if complaint_info['eNodbe_number'] not in item:
                vol_drop_put(complaint_info, session_vol)
            else:
                updata_vol_drop(complaint_info, session_vol)
            return render_template('put_vol_drop_succ.html',
                                   complaint_info=complaint_info)
    return render_template('vol_drop_detail.html', cell_name=cell_name, rrc_fail_count_options=rrc_fail_count.dump_options(),
                            recon_count_chart_options=recon_count_chart.dump_options(),recon_ratio_chart_options=recon_ratio_chart.dump_options(),form=form)



@app.route("/volte drop")
def show_volte_drop():
    qtem_vol = session_kpi.execute(
        "select 时间,VoLTE语音掉话率 from(select 时间,VoLTE语音掉话率 from kpi_summary_vol_nb where 厂家='不区分厂家' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_vol = list(qtem_vol)
    qtem_vol_x_axis = [x.时间 for x in qtem_vol]
    qtem_vol_data = [round(x.VoLTE语音掉话率,2) for x in qtem_vol]
    qw_rrc = draw_line(qtem_vol_x_axis, '全网VoLTE语音掉话率', qtem_vol_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,VoLTE语音掉话率 from(select 时间,VoLTE语音掉话率 from kpi_summary_vol_nb where 厂家='中兴' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [round(x[1],2) for x in item_rrc1]
    zte_rrc = draw_line( item_rrc_x_axis, '中兴', item_rrc_800_data, '中兴')

    rtem_rrc = session_kpi.execute(
        "select 时间,VoLTE语音掉话率 from(select 时间,VoLTE语音掉话率 from kpi_summary_vol_nb where 厂家='爱立信' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data =  [round(x[1],2) for x in rtem_rrc1]
    eri_rrc = draw_line( rtem_rrc_x_axis, '爱立信', rtem_rrc_800_data, '爱立信')

    htem_rrc = session_kpi.execute(
        "select 时间,VoLTE语音掉话率 from(select 时间,VoLTE语音掉话率 from kpi_summary_vol_nb where 厂家='华为' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    htem_rrc1 = list(htem_rrc)
    htem_rrc_x_axis = [x[0] for x in htem_rrc1]
    htem_rrc_data =  [round(x[1],2) for x in htem_rrc1]
    hw_rrcc = draw_line(htem_rrc_x_axis, '华为', htem_rrc_data, '华为', )

    return render_template('vol_drop_report.html', zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(), qw_rrc_options=qw_rrc.dump_options())

@app.route("/nb rate")
def show_nb_rate():
    vtem_nb = session_kpi.execute(
        "select 时间,NB_IoT小区RRC连接建立请求次数,NB_IoT小区RRC连接建立失败总次数 FROM (select 时间,NB_IoT小区RRC连接建立请求次数,NB_IoT小区RRC连接建立失败总次数 from kpi_summary_vol_nb where 厂家='不区分厂家' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    vtem_nb = list(vtem_nb)
    vtem_nb_x_axis = [x.时间 for x in vtem_nb]
    vtem_nb_requ1 = [x.NB_IoT小区RRC连接建立请求次数 for x in vtem_nb]
    vtem_nb_requ2 = [x.NB_IoT小区RRC连接建立失败总次数 for x in vtem_nb]
    nb_request = draw_bar2('全网NB_IoT小区RRC连接建立请求次数','NB_IoT小区RRC连接建立失败总次数',   vtem_nb_requ1,vtem_nb_requ2,
                            vtem_nb_x_axis,
                            '全市NB_IoT小区RRC连接次数')

    qtem_vol = session_kpi.execute(
        "select 时间,NB_IoT小区RRC连接建立成功率 from(select 时间,NB_IoT小区RRC连接建立成功率 from kpi_summary_vol_nb where 厂家='不区分厂家' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    qtem_vol = list(qtem_vol)
    qtem_vol_x_axis = [x.时间 for x in qtem_vol]
    qtem_vol_data = [round(x.NB_IoT小区RRC连接建立成功率*100,2) for x in qtem_vol]
    qw_rrc = draw_line(qtem_vol_x_axis, '全网NB_IoT小区RRC连接建立成功率', qtem_vol_data, '全网指标', )

    item_rrc = session_kpi.execute(
        "select 时间,NB_IoT小区RRC连接建立成功率 from(select 时间,NB_IoT小区RRC连接建立成功率 from kpi_summary_vol_nb where 厂家='中兴' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    item_rrc1 = list(item_rrc)
    item_rrc_x_axis = [x[0] for x in item_rrc1]
    item_rrc_800_data = [round(x[1]*100,2) for x in item_rrc1]
    zte_rrc = draw_line( item_rrc_x_axis, '中兴', item_rrc_800_data, '中兴')

    rtem_rrc = session_kpi.execute(
        "select 时间,NB_IoT小区RRC连接建立成功率 from(select 时间,NB_IoT小区RRC连接建立成功率 from kpi_summary_vol_nb where 厂家='爱立信' order by 时间 DESC LIMIT 20)aa ORDER BY 时间 asc")
    session_kpi.close()
    rtem_rrc1 = list(rtem_rrc)
    rtem_rrc_x_axis = [x[0] for x in rtem_rrc1]
    rtem_rrc_800_data = [round(x[1]*100,2) for x in rtem_rrc1]
    eri_rrc = draw_line( rtem_rrc_x_axis, '爱立信', rtem_rrc_800_data, '爱立信')

    return render_template('nb_rate_report.html', nb_request_options=nb_request.dump_options(),zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           qw_rrc_options=qw_rrc.dump_options())

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
    cell_name =  session_rrc.execute("SELECT `小区名称` FROM `rrc重建` where `站号` = {enb} and `小区号` = {cell}".format(enb=enb, cell=cell))
    cell_name = list(cell_name)
    cell_name = cell_name[0].小区名称
    weeks = session_rrc.execute("SELECT DISTINCT week(`日期`) from `rrc重建`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week = session_rrc.execute("SELECT max(week(`日期`)) from `rrc重建`")
    cur_week = list(cur_week)[0][0]
    return render_template('hand_over.html',
                           zte_rrc_options=zte_rrc.dump_options(),
                           eri_rrc_options=eri_rrc.dump_options(),
                           hw_rrcc_options=hw_rrcc.dump_options(),
                           qw_rrc_options=qw_rrc.dump_options())

@app.route("/school/", methods=['GET', 'POST'])
def school():
    month = session_mr.execute("select DISTINCT month(date_time) as 'month' from mr_summary")
    month = list(month)
    month = [x.month for x in month]
    month = int(max(month))
    cur_week = session_kpi.execute("SELECT max(week(`日期`)) from `zte_day_{}`".format(month))
    cur_week = list(cur_week)[0][0]
    top_cells = session_kpi.execute(
        "SELECT 校园名称,sum(上行流量)as 上行流量, sum(下行流量) as 下行流量,avg(下行体验速率)as 下行体验速率, avg(用户面下行包平均时延)as 用户面下行包平均时延, avg(上行prb利用率)as 上行prb利用率, avg(下行prb利用率)as 下行prb利用率,avg(b.上行体验速率)as 上行体验速率 FROM (SELECT * FROM school) as a inner JOIN (SELECT 小区名称,最大RRC连接用户数,上行流量,下行流量,上行体验速率,下行体验速率,用户面下行包平均时延,上行prb利用率,下行prb利用率 FROM zte_day_{b} WHERE WEEK(日期,3)={cur_week}) as b ON a.小区名称=b.小区名称 GROUP BY 校园名称".format(cur_week=cur_week,b=month))
    session_kpi.close()
    cells = list(top_cells)
    school_ul = [round(x.上行流量/1024/1024,2) for x in cells]
    school_dl = [round(x.下行流量/1024/1024,2) for x in cells]

    school_time = [round(x.用户面下行包平均时延,2) for x in cells]

    school_uprb = [round(x.上行prb利用率*100,2)for x in cells]
    school_dprb = [round(x.下行prb利用率*100,2)for x in cells]

    school_ufell = [round(x.上行体验速率,2) for x in cells]
    school_dfell = [round(x.下行体验速率,2) for x in cells]
    school_name = [x.校园名称 for x in cells]

    school_ll_p=draw_bar2('上行流量', '下行流量', school_ul, school_dl, school_name, '上下行流量（TB）')
    school_time_p = draw_bar('下行用户面时延', school_time, school_name, '校园下行用户面时延(ms)')
    school_prb_p = draw_bar2('上行prb利用率', '下行prb利用率', school_uprb, school_dprb, school_name, 'prb利用率（%）')
    school_fell_p = draw_bar2('上行用户体验速率', '下行用户体验速率', school_ufell, school_dfell, school_name, '上下行体验速率（Mb/s）')

    top_cells_info = [x for x in school_name]
    return render_template('rrc_school.html',top_cells_info=top_cells_info,cur_week=cur_week,
                           school_ll_p_options=school_ll_p.dump_options(),
                            school_time_p_options = school_time_p.dump_options(),
                            school_prb_p_options = school_prb_p.dump_options(),
                           school_fell_p_options=school_fell_p.dump_options())


@app.route("/school/<school_name>", methods=['GET', 'POST'])
def school_list(school_name):
    month = session_mr.execute("select DISTINCT month(date_time) as 'month' from mr_summary")
    month = list(month)
    month = [x.month for x in month]
    month = int(max(month))
    cur_week = session_kpi.execute("SELECT max(week(`日期`)) from `zte_day_{}`".format(month))
    cur_week = list(cur_week)[0][0]
    top_cells = session_kpi.execute("SELECT 日期,校园名称,sum(最大RRC连接用户数)as 最大RRC连接用户数,sum(上行流量)as 上行流量, sum(下行流量) as 下行流量,avg(下行体验速率)as 下行体验速率, avg(用户面下行包平均时延)as 用户面下行包平均时延, avg(上行prb利用率)as 上行prb利用率, avg(下行prb利用率)as 下行prb利用率,avg(b.上行体验速率)as 上行体验速率 FROM (SELECT * FROM school WHERE 校园名称='{school_name}') as a inner JOIN (SELECT 日期,小区名称,最大RRC连接用户数,上行流量,下行流量,上行体验速率,下行体验速率,用户面下行包平均时延,上行prb利用率,下行prb利用率 FROM zte_day_{b} WHERE WEEK(日期,3)={cur_week}) as b ON a.小区名称=b.小区名称 GROUP BY 校园名称,日期".format(cur_week=cur_week,school_name=school_name,b=month))
    session_kpi.close()
    cells = list(top_cells)
    school_ul = [round(x.上行流量/1024/1024, 2) for x in cells]
    school_dl = [round(x.下行流量/1024/1024, 2) for x in cells]

    school_time = [round(x.用户面下行包平均时延, 2) for x in cells]
    school_ue = [x.最大RRC连接用户数 for x in cells]

    school_uprb = [round(x.上行prb利用率*100, 2) for x in cells]
    school_dprb = [round(x.下行prb利用率*100, 2) for x in cells]

    school_ufell = [round(x.上行体验速率, 2) for x in cells]
    school_dfell = [round(x.下行体验速率, 2) for x in cells]
    school_data = [x.日期 for x in cells]

    school_time_p = draw_bar('下行用户面时延', school_time, school_data, '校园下行用户面时延(ms)')
    school_ue_p = draw_bar('最大RRC连接用户数', school_ue, school_data, '最大RRC连接用户数(户)')

    school_ll_p = draw_bar2('上行流量', '下行流量', school_ul, school_dl, school_data, '上下行流量（TB）')
    school_prb_p = draw_bar2('上行prb利用率', '下行prb利用率', school_uprb, school_dprb, school_data, 'prb利用率（%）')
    school_fell_p = draw_bar2('上行用户体验速率', '下行用户体验速率', school_ufell, school_dfell, school_data, '上下行体验速率（Mb/s）')

    return render_template('rrc_school_every.html',
                                school_name=school_name,
                                cur_week=cur_week,
                                school_ll_p_options=school_ll_p.dump_options(),
                                school_ue_p_options=school_ue_p.dump_options(),
                                school_time_p_options = school_time_p.dump_options(),
                                school_prb_p_options = school_prb_p.dump_options(),
                               school_fell_p_options=school_fell_p.dump_options())



if __name__ == "__main__":
    app.run()