from flask import Flask, render_template, request, redirect, url_for
from config import Config
from forms import Delete_bts_form, Complaint_form, Work_report_form,Department_work_report_form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from func import put2base, updata2base
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['zip'] = zip

engine_tousu = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/qjwx_tousu?charset=utf8",
                             pool_recycle=7200)
engine_del = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/delete_bts?charset=utf8", pool_recycle=7200)
engine_work = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/work_report?charset=utf8",
                            pool_recycle=7200)

Session_del = sessionmaker(autocommit=False, autoflush=True, bind=engine_del)
Session_tousu = sessionmaker(autocommit=False, autoflush=True, bind=engine_tousu)
Session_work = sessionmaker(autocommit=False, autoflush=True, bind=engine_work)

session_del = Session_del()
session_tousu = Session_tousu()
session_work = Session_work()


@app.route('/del', methods=['GET', 'POST'])
def delbts2datebase():
    # 将表单类实例化
    form = Delete_bts_form()
    table_titles = ['网管名称', '设备类型', '基站代码', '网管基站名称', '删除原因', '删除时间', 'BBU是否拆除', 'RRU是否拆除', '天线是否拆除']

    del_data = session_del.execute("SELECT * from `网管删除的基站`")
    del_data = list(del_data)
    omc = [x.omc for x in del_data]
    work_type = [x.work_type for x in del_data]
    btsid = [x.btsid for x in del_data]
    btsname = [x.btsname for x in del_data]
    reason = [x.reason for x in del_data]
    shuttime = [x.shuttime for x in del_data]
    bbustate = [x.bbustate for x in del_data]
    rrustate = [x.rrustate for x in del_data]
    antstate = [x.antstate for x in del_data]
    session_del.close()

    if request.method == 'POST':
        if form.validate_on_submit():
            delete_bts_info = request.form.to_dict()
            reason_dict = {'0': '停电', '1': '光缆断', '2': '设备故障', '3': '站址搬迁', '4': '物业纠纷', '5': '学校放假'}
            omc = delete_bts_info.get('omc')
            work_type = delete_bts_info.get('work_type')
            btsid = delete_bts_info.get('btsid')
            btsname = delete_bts_info.get('btsname')
            reason_code = delete_bts_info.get('reason')
            reason = reason_dict.get(reason_code)
            shuttime = delete_bts_info.get('shuttime')
            bbustate = delete_bts_info.get('bbustate')
            rrustate = delete_bts_info.get('rrustate')
            antstate = delete_bts_info.get('antstate')
            session_del.execute(
                "INSERT INTO  `网管删除的基站`(`omc`, `work_type`, `btsid`, `btsname`, `reason`, `shuttime`,`bbustate`,`rrustate`,`antstate`) VALUES ('{om}','{ty}','{id}','{na}','{re}','{sh}','{bb}','{rr}','{an}')".format(
                    om=omc, ty=work_type, id=btsid, na=btsname, re=reason, sh=shuttime, bb=bbustate, rr=rrustate,
                    an=antstate))
            session_del.commit()
            session_del.close()

            return render_template('delbts_put_succ.html',
                                   table_titles=table_titles,
                                   omc=omc,
                                   work_type=work_type,
                                   btsid=btsid,
                                   btsname=btsname,
                                   reason=reason,
                                   shuttime=shuttime,
                                   bbustate=bbustate,
                                   rrustate=rrustate,
                                   antstate=antstate
                                   )
    return render_template('del_bts2database.html',
                           form=form,
                           table_titles=table_titles,
                           omc=omc,
                           work_type=work_type,
                           btsid=btsid,
                           btsname=btsname,
                           reason=reason,
                           shuttime=shuttime,
                           bbustate=bbustate,
                           rrustate=rrustate,
                           antstate=antstate
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

@app.route('/work/', methods=['GET', 'POST'])
def show_department_work():
    # 将表单类实例化
    week = int(pd.to_datetime(datetime.now()).strftime("%V"))
    form = Department_work_report_form()

    table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']

    work_data = session_work.execute("SELECT * from `工作周报` where `周` = {wk} order by `姓名`,`开始日期` asc ".format(wk=week))
    work_data = list(work_data)

    weeks = [x.周 for x in work_data]
    realnames = [x.姓名 for x in work_data]
    start_date = [x.开始日期 for x in work_data]
    end_date = [x.结束日期 for x in work_data]
    work_type = [x.工作类别 for x in work_data]
    content = [x.工作内容 for x in work_data]
    state = [x.当前状态 for x in work_data]
    session_work.close()

    if request.method == 'POST':
        if form.validate_on_submit():
            work_info = request.form.to_dict()
            c_week = work_info.get('week')
            s_name = work_info.get('name')
            s_date = work_info.get('start_date')
            e_date = work_info.get('end_date')
            w_type = work_info.get('work_type')
            w_content = work_info.get('content')
            w_state = work_info.get('state')

            session_work.execute(
                "INSERT INTO  `工作周报`(`周`,`姓名`, `开始日期`, `结束日期`, `工作类别`, `工作内容`, `当前状态`) VALUES ('{wk}','{na}','{sd}','{ed}','{ty}','{co}','{st}')".format(
                    wk=c_week, na=s_name, sd=s_date, ed=e_date, ty=w_type, co=w_content, st=w_state))
            session_work.commit()
            session_work.close()

            return render_template('department_put_succ.html',
                                   table_titles=table_titles,
                                   week=c_week,
                                   realname=s_name,
                                   start_date=s_date,
                                   end_date=e_date,
                                   work_type=w_type,
                                   content=w_content,
                                   state=w_state
                                   )

    return render_template('department_work2database.html',
                           staffname='无线中心',
                           form=form,
                           table_titles=table_titles,
                           weeks=weeks,
                           realnames=realnames,
                           start_date=start_date,
                           end_date=end_date,
                           work_type=work_type,
                           content=content,
                           state=state
                           )


@app.route('/work/<name>', methods=['GET', 'POST'])
def work2datebase(name):
    # 将表单类实例化
    week = int(pd.to_datetime(datetime.now()).strftime("%V"))
    name_dict = {
        'qjwx': '无线中心',
        'fms': '冯明山',
        'wx': '王鑫',
        'zcc': '周朝成',
        'tzy': '田中玉',
        'xyg': '解艳刚',
        'syl': '史艳丽',
        'ztx': '查天星'
    }
    real_name = name_dict.get(name)
    form = Work_report_form()

    table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']
    if name == 'qjwx':
        work_data = session_work.execute("SELECT * from `工作周报` where `周` = {wk} order by `姓名`,`开始日期` asc ".format(wk=week))
    else:
        work_data = session_work.execute(
            "SELECT * from `工作周报` where `姓名` = '{na}' and `周` = {wk}".format(na=real_name, wk=week))
    work_data = list(work_data)
    weeks = [x.周 for x in work_data]
    realnames = [x.姓名 for x in work_data]
    start_date = [x.开始日期 for x in work_data]
    end_date = [x.结束日期 for x in work_data]
    work_type = [x.工作类别 for x in work_data]
    content = [x.工作内容 for x in work_data]
    state = [x.当前状态 for x in work_data]
    session_work.close()

    if request.method == 'POST':
        if form.validate_on_submit():
            work_info = request.form.to_dict()
            s_date = work_info.get('start_date')
            e_date = work_info.get('end_date')
            w_type = work_info.get('work_type')
            w_content = work_info.get('content')
            w_state = work_info.get('state')

            session_work.execute(
                "INSERT INTO  `工作周报`(`周`,`姓名`, `开始日期`, `结束日期`, `工作类别`, `工作内容`, `当前状态`) VALUES ('{wk}','{na}','{sd}','{ed}','{ty}','{co}','{st}')".format(
                    wk=week, na=real_name, sd=s_date, ed=e_date, ty=w_type, co=w_content, st=w_state))
            session_work.commit()
            session_work.close()

            return render_template('work_put_succ.html',
                                   table_titles=table_titles,
                                   staff_name = name,
                                   week=week,
                                   realname=real_name,
                                   start_date=s_date,
                                   end_date=e_date,
                                   work_type=w_type,
                                   content=w_content,
                                   state=w_state
                                   )
    return render_template('work_put2database.html',
                           staffname=real_name,
                           form=form,
                           table_titles=table_titles,
                           weeks=weeks,
                           realnames=realnames,
                           start_date=start_date,
                           end_date=end_date,
                           work_type=work_type,
                           content=content,
                           state=state
                           )


if __name__ == '__main__':
    app.run(debug=True)
