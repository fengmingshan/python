from flask import Flask, url_for, request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tousu
from forms import Complaint_form, Select_form
from config import Config
from func import draw_bar, draw_line3, draw_line2, draw_line, draw_pie,draw_bar_reversal,draw_bar2_reversal
from func import put2base, updata2base

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
    pro = draw_bar('全网', pro_y_data, pro_x_axis, '全省各州市MR全网指标对比')

    pro_data_not800 = session_cqi.execute(
        "select area,round(abpve7_rate,4)*100 from cqi_summary where static_zone = '1800M' and month(date_time) = {month} group by area order by round(abpve7_rate,4)*100 desc".format(
            month=month))
    pro_data_not800 = list(pro_data_not800)
    pro_x_axis_not800 = [x[0] for x in pro_data_not800]
    pro_y_data_not800 = [x[1] for x in pro_data_not800]
    pro_not800 = draw_bar('L1800', pro_y_data_not800, pro_x_axis_not800, '全省各州市L1800网络MR指标')

    pro_data_800 = session_cqi.execute(
        "select area,round(abpve7_rate,4)*100 from cqi_summary where static_zone = '800M' and month(date_time) = {month} group by area order by round(abpve7_rate,4)*100 desc".format(
            month=month))
    pro_data_800 = list(pro_data_800)
    pro_x_axis_800 = [x[0] for x in pro_data_800]
    pro_y_data_800 = [x[1] for x in pro_data_800]
    pro_800 = draw_bar('800M', pro_y_data_800, pro_x_axis_800, '全省各州市800M网络MR指标')

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
    qj = draw_line3('曲靖全市两网指标对比', qj_x_axis, '曲靖全月', qj_y_data, '曲靖1800M', qj1800_y_data, '曲靖800M', qj800_y_data)

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
    zte = draw_line3('中兴两网指标对比', zte_all_x_axis, '中兴全网MR指标', zte_all_y_data, '中兴1800M', zte1800_y_data, '中兴800M',
                     zte800_y_data)

    eric800_data = session_cqi.execute(
        "select date_time,abpve7_rate from cqi_summary where area = '曲靖市' and static_zone = '爱立信800M' and month(date_time) = {month} order by date_time asc".format(
            month=month))
    session_cqi.close()
    eric800_data = list(eric800_data)
    eric800_x_axis = [x[0] for x in eric800_data]
    eric800_y_data = [round(x[1] * 100, 2) for x in eric800_data]
    eric_zte = draw_line2('爱立信中兴800M指标对比', eric800_x_axis, '爱立信800M', eric800_y_data, '中兴800M', zte800_y_data)
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


@app.route("/rrc_recon_top/", methods=['GET', 'POST'])
def show_rrc_recon_list():
    cur_week = session_rrc.execute("SELECT max(week(`开始时间`)) from `rrc重建`")
    cur_week = list(cur_week)[0][0]
    top_cells = session_rrc.execute(
        "SELECT eNodeB, `小区`, `小区名称`, `RRC重建请求数目`, a.rrc_recon_ratio, a.rrc_recon_count/b.rrc_recon_sum as '占全网比例' FROM (SELECT eNodeB, `小区`, `小区名称`, week(`开始时间`) as 'week', `RRC重建请求数目`, `RRC重建立比例` as 'rrc_recon_ratio', `RRC重建请求数目` as 'rrc_recon_count' from `rrc重建`) as a, (SELECT sum(`RRC重建请求数目`) as 'rrc_recon_sum' from `rrc重建`) as b WHERE a.`week` = {cur_week} ORDER BY a.rrc_recon_count/b.rrc_recon_sum DESC LIMIT 20".format(
            cur_week=cur_week))
    top_cells = list(top_cells)
    top_cells_name = [x.小区名称 for x in top_cells]
    top_cells_enb = [x.eNodeB for x in top_cells]
    top_cells_cell = [x.小区 for x in top_cells]
    top_cells_info = [str(x) + "_" + str(y) for x, y in zip(top_cells_enb, top_cells_cell)]
    return render_template('rrc_recon_list.html', top_cells_info=top_cells_info, top_cells_name=top_cells_name)


@app.route("/rrc_recon_top/<cell_info>", methods=['GET', 'POST'])
def show_rrc_recon_detail(cell_info):
    enb = cell_info.split('_')[0]
    cell = cell_info.split('_')[1]
    cell_name =  session_rrc.execute("SELECT `小区名称` FROM `rrc重建` where `eNodeB` = {enb} and `小区` = {cell}".format(enb=enb, cell=cell))
    cell_name = list(cell_name)
    cell_name = cell_name[0].小区名称
    weeks = session_rrc.execute("SELECT DISTINCT week(`开始时间`) from `rrc重建`")
    weeks = list(weeks)
    weeks = [x[0] for x in weeks]
    cur_week = session_rrc.execute("SELECT max(week(`开始时间`)) from `rrc重建`")
    cur_week = list(cur_week)[0][0]

    recon_ratio = session_rrc.execute(
        "SELECT eNodeB, `小区`, `RRC重建立比例`, `RRC重建请求数目` FROM `rrc重建` where eNodeB = {enb} and `小区` ={cell} and week(`开始时间`) = {week}".format(
            enb=enb, cell=cell, week=cur_week))
    recon_ratio = list(recon_ratio)
    ratio = [float(x[2].replace('%', '')) for x in recon_ratio]
    recon_count = [x[3] for x in recon_ratio]
    recon_ratio_chart = draw_line(weeks,'RRC重建比例', ratio, 'RRC重建比例')
    recon_count_chart = draw_bar('RRC重建请求次数', recon_count,  weeks, 'RRC重建次数',)

    recon_reason = session_rrc.execute(
        "SELECT eNodeB, `小区`, `RRC重建请求数目`, `切换失败触发的RRC重建立请求次数`, `其它原因触发的RRC重建立请求次数`, `重配失败触发的RRC重建立请求次数` FROM `rrc重建` where eNodeB = {enb} and `小区` ={cell} and week(`开始时间`) = {week}".format(
            enb=enb, cell=cell, week=cur_week))
    recon_reason = list(recon_reason)[0]
    recon_reason = recon_reason[3:]
    recon_reason_chart = draw_pie(['切换失败','其它原因','重配失败'],recon_reason,'RRC重建原因:','RRC重建原因')

    return render_template('rrc_recon_detail.html', cell_name = cell_name,rrc_recon_reason_chart_options=recon_reason_chart.dump_options(),rrc_recon_ratio_chart_options=recon_ratio_chart.dump_options(),rrc_recon_count_chart_options=recon_count_chart.dump_options())


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
