from flask import Flask, render_template, request, redirect, url_for
from config import Config
from forms import Delete_bts_form, Complaint_form, Work_report_form, Plan_work_form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from func import put2base, updata2base
from datetime import datetime

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
    type = [x.type for x in del_data]
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
            type = delete_bts_info.get('type')
            btsid = delete_bts_info.get('btsid')
            btsname = delete_bts_info.get('btsname')
            reason_code = delete_bts_info.get('reason')
            reason = reason_dict.get(reason_code)
            shuttime = delete_bts_info.get('shuttime')
            bbustate = delete_bts_info.get('bbustate')
            rrustate = delete_bts_info.get('rrustate')
            antstate = delete_bts_info.get('antstate')
            session_del.execute(
                "INSERT INTO  `网管删除的基站`(`omc`, `type`, `btsid`, `btsname`, `reason`, `shuttime`,`bbustate`,`rrustate`,`antstate`) VALUES ('{om}','{ty}','{id}','{na}','{re}','{sh}','{bb}','{rr}','{an}')".format(
                    om=omc, ty=type, id=btsid, na=btsname, re=reason, sh=shuttime, bb=bbustate, rr=rrustate,
                    an=antstate))
            session_del.commit()
            session_del.close()

            return render_template('delbts_put_succ.html',
                                   table_titles=table_titles,
                                   omc=omc,
                                   type=type,
                                   btsid=btsid,
                                   btsname=btsname,
                                   reason=reason,
                                   shuttime=shuttime,
                                   bbustate=bbustate,
                                   rrustate=rrustate,
                                   antstate=antstate
                                   )
    return render_template('delbts_index.html',
                           form=form,
                           table_titles=table_titles,
                           omc=omc,
                           type=type,
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
            return render_template('tousu_put_succ.html', complaint_info=complaint_info)
    return render_template('tousu_form.html', form=form)


@app.route('/work/', methods=['GET', 'POST'])
def show_department_work():
    # 将表单类实例化
    week = datetime.now().date().isocalendar()[1]
    form = Plan_work_form()

    work_data = session_work.execute("SELECT * from `工作周报` where `周` = {wk} and `工作类别` != '安排的工作' order by `姓名`,`开始日期` asc ".format(wk=week))
    work_data = list(work_data)
    weeks = [x.周 for x in work_data]
    realnames = [x.姓名 for x in work_data]
    start_date = [x.开始日期 for x in work_data]
    end_date = [x.结束日期 for x in work_data]
    work_type = [x.工作类别 for x in work_data]
    content = [x.工作内容 for x in work_data]
    state = [x.当前状态 for x in work_data]
    session_work.close()

    plan_work_data = session_work.execute(
        "SELECT * from `工作周报` where `周` = {wk} and `工作类别` = '安排的工作' order by `姓名`,`开始日期` asc ".format(wk=week)
    )
    plan_work_data = list(plan_work_data)
    p_weeks = [x.周 for x in plan_work_data]
    p_realnames = [x.姓名 for x in plan_work_data]
    p_start_date = [x.开始日期 for x in plan_work_data]
    p_end_date = [x.结束日期 for x in plan_work_data]
    p_work_type = [x.工作类别 for x in plan_work_data]
    p_content = [x.工作内容 for x in plan_work_data]
    p_state = [x.当前状态 for x in plan_work_data]

    if request.method == 'POST':
        if form.validate_on_submit():
            plan_info = request.form.to_dict()
            c_week = week
            s_name = plan_info.get('name')
            s_date = plan_info.get('start_date')
            e_date = '9999-09-09'
            w_type = '安排的工作'
            w_content = plan_info.get('content')
            w_content = w_content.strip().replace(' ', '')
            w_state = '待反馈'

            session_work.execute(
                "INSERT INTO  `工作周报`(`周`,`姓名`, `开始日期`,`结束日期`,`工作类别`,`工作内容`,`当前状态`) VALUES ({wk},'{na}','{sd}','{ed}','{ty}','{co}','{st}')".format(
                    wk=c_week, na=s_name, sd=s_date, ed=e_date, ty=w_type, co=w_content ,st=w_state))
            session_work.commit()
            session_work.close()

            schedule_titles = ['周', '姓名', '开始日期', '工作类别', '工作内容']
            return render_template('department_put_succ.html',
                                   schedule_titles=schedule_titles,
                                   week=c_week,
                                   realname=s_name,
                                   start_date=s_date,
                                   work_type=w_type,
                                   content=w_content,
                                   )

    table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']
    return render_template('department_work2database.html',
                           form=form,
                           table_titles=table_titles,
                           weeks=weeks,
                           realnames=realnames,
                           start_date=start_date,
                           end_date=end_date,
                           work_type=work_type,
                           content=content,
                           state=state,
                           p_weeks=p_weeks,
                           p_realnames=p_realnames,
                           p_start_date=p_start_date,
                           p_end_date=p_end_date,
                           p_work_type=p_work_type,
                           p_content=p_content,
                           p_state=p_state
                           )


@app.route('/work/<name>', methods=['GET', 'POST'])
def work2datebase(name):
    # 将表单类实例化
    week = datetime.now().date().isocalendar()[1]
    name_dict = {
        'qjwx': '无线中心',
        'fms': '冯明山',
        'wx': '王鑫',
        'zcc': '周朝城',
        'tzy': '田中玉',
        'xyg': '解艳刚',
        'syl': '史艳丽',
        'ztx': '查天星'
    }
    table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']
    real_name = name_dict.get(name)
    form = Work_report_form()

    plan_work_data = session_work.execute(
        "SELECT * from `工作周报` where `姓名` = '{na}' and `周` = {wk} and `工作类别` = '安排的工作'".format(na=real_name,
                                                                                              wk=week))
    work_data = session_work.execute(
        "SELECT * from `工作周报` where `姓名` = '{na}' and `周` = {wk} and `工作类别` != '安排的工作'".format(na=real_name,
                                                                                               wk=week))
    plan_work_data = list(plan_work_data)
    p_weeks = [x.周 for x in plan_work_data]
    p_realnames = [x.姓名 for x in plan_work_data]
    p_start_date = [x.开始日期 for x in plan_work_data]
    p_end_date = [x.结束日期 for x in plan_work_data]
    p_work_type = [x.工作类别 for x in plan_work_data]
    p_content = [x.工作内容 for x in plan_work_data]
    p_state = [x.当前状态 for x in plan_work_data]

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
            w_content = w_content.strip().replace(' ', '')
            w_content = w_content.strip().replace('\t', '')
            w_state = work_info.get('state')

            session_work.execute(
                "INSERT INTO  `工作周报`(`周`,`姓名`, `开始日期`, `结束日期`, `工作类别`, `工作内容`, `当前状态`) VALUES ({wk},'{na}','{sd}','{ed}','{ty}','{co}','{st}')".format(
                    wk=week, na=real_name, sd=s_date, ed=e_date, ty=w_type, co=w_content, st=w_state))
            session_work.commit()
            session_work.close()

            return render_template('work_put_succ.html',
                                   table_titles=table_titles,
                                   name=name,
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
                           state=state,
                           p_weeks=p_weeks,
                           p_realnames=p_realnames,
                           p_start_date=p_start_date,
                           p_end_date=p_end_date,
                           p_work_type=p_work_type,
                           p_content=p_content,
                           p_state=p_state
                           )


@app.route('/work/up/', methods=['GET', 'POST'])
def update_work():
    rev_name_dict = {
        '无线中心': 'qjwx',
        '冯明山': 'fms',
        '王鑫': 'wx',
        '周朝城': 'zcc',
        '田中玉': 'tzy',
        '解艳刚': 'xyg',
        '史艳丽': 'syl',
        '查天星': 'ztx'
    }

    table_data = request.args.to_dict()
    source = table_data.get('source')
    week = table_data.get('wk')
    realname = table_data.get('na')
    stratdate = table_data.get('sd')
    stratdate_date = datetime.strptime(stratdate, '%Y-%m-%d')
    enddate = table_data.get('ed') if table_data.get('ed') != 'None' else '9999-09-09'
    enddate_date = datetime.strptime(enddate, '%Y-%m-%d')
    worktype = table_data.get('ty')
    ori_content = table_data.get('co')
    workstate = table_data.get('st') if table_data.get('ed') != 'None' else '进行中'

    form = Work_report_form()

    form.start_date.data = stratdate_date
    form.end_date.data = enddate_date
    form.work_type.data = worktype
    form.content.data = ori_content
    form.state.data = workstate

    if source == 'person':
        name = rev_name_dict.get(realname)
    elif source == 'department':
        name = ''

    if request.method == 'POST':
        if form.validate_on_submit():
            work_info = request.form.to_dict()
            s_date = work_info.get('start_date')
            e_date = work_info.get('end_date')
            w_type = work_info.get('work_type')
            w_content = work_info.get('content')
            w_state = work_info.get('state')

            session_work.execute(
                "UPDATE `工作周报` SET `周` = '{wk}' ,`开始日期` = '{sd}' ,`结束日期` = '{ed}' ,`工作类别` = '{nty}' ,`工作内容` = '{co}' , `当前状态` = '{st}' WHERE `姓名` = '{na}' AND `开始日期` = '{date}' AND `工作类别` = '{ty}' AND  `工作内容` = '{ori_content}'".format(
                    wk=week, sd=s_date, ed=e_date, nty=w_type, co=w_content, st=w_state, na=realname, date=stratdate,ty=worktype,
                    ori_content=ori_content))
            session_work.commit()
            session_work.close()

            table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']
            return render_template('work_put_succ.html',
                                   table_titles=table_titles,
                                   name=name,
                                   week=week,
                                   realname=realname,
                                   start_date=s_date,
                                   end_date=e_date,
                                   work_type=w_type,
                                   content=w_content,
                                   state=w_state,
                                   )
    return render_template('update_work.html',
                           name=name,
                           form=form,
                           staffname=realname,
                           workstate=workstate
                           )


@app.route('/work/delconfirm/', methods=['GET', 'POST'])
def delete_work_confirm():
    rev_name_dict = {
        '无线中心': 'qjwx',
        '冯明山': 'fms',
        '王鑫': 'wx',
        '周朝城': 'zcc',
        '田中玉': 'tzy',
        '解艳刚': 'xyg',
        '史艳丽': 'syl',
        '查天星': 'ztx'
    }
    table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']

    table_data = request.args.to_dict()
    source = table_data.get('source')
    week = table_data.get('wk')
    realname = table_data.get('na')
    stratdate = table_data.get('sd')
    worktype = table_data.get('ty')
    content = table_data.get('co')

    if source == 'person':
        name = rev_name_dict.get(realname)
        enddate = table_data.get('ed')
        workstate = table_data.get('st')
    elif source == 'department':
        name = ''
        enddate = '9999-09-09'
        workstate = '待反馈'

    return render_template('work_delete_confirm.html',
                           name=name,
                           source = source,
                           table_titles=table_titles,
                           week=week,
                           realname=realname,
                           start_date=stratdate,
                           end_date=enddate,
                           work_type=worktype,
                           work_content=content,
                           work_state=workstate
                           )


@app.route('/work/del/', methods=['GET', 'POST'])
def delete_work():
    rev_name_dict = {
        '无线中心': 'qjwx',
        '冯明山': 'fms',
        '王鑫': 'wx',
        '周朝城': 'zcc',
        '田中玉': 'tzy',
        '解艳刚': 'xyg',
        '史艳丽': 'syl',
        '查天星': 'ztx'
    }

    table_data = request.args.to_dict()
    source = table_data.get('source')
    realname = table_data.get('na')
    stratdate = table_data.get('sd')
    enddate = table_data.get('ed')
    worktype = table_data.get('ty')
    content = table_data.get('co')
    workstate = table_data.get('st')

    if source == 'person':
        name = rev_name_dict.get(realname)
    elif source == 'department':
        name = ''

    session_work.execute(
        "DELETE FROM `工作周报` WHERE `姓名` = '{na}' AND `开始日期` = '{sd}' AND `结束日期` = '{ed}' AND `工作类别` = '{ty}' AND `工作内容` = '{co}' AND `当前状态` = '{st}'".format(
            na=realname, sd=stratdate, ed=enddate, ty=worktype, co=content, st=workstate))
    session_work.commit()

    return redirect(url_for('work2datebase',name = name))

if __name__ == '__main__':
    app.run(debug=True,port = 8002)
