from flask import Flask, render_template, request, redirect, url_for
from config import Config
from forms import Work_report_form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

@app.route('/up/', methods=['GET', 'POST'])
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
    week = table_data.get('wk')
    realname = table_data.get('na')
    stratdate = table_data.get('sd')
    stratdate = datetime.strptime(stratdate, '%Y-%m-%d')
    stratdate_str = str(stratdate).split(' ')[0]
    enddate = '9999-09-09'
    enddate = datetime.strptime(enddate, '%Y-%m-%d')
    worktype = table_data.get('ty')
    content = table_data.get('co')
    workstate = '进行中'

    form = Work_report_form()

    form.start_date.data = stratdate
    form.end_date.data = enddate
    form.work_type.data = worktype
    form.content.data = content
    form.state.data = workstate

    staff_name = rev_name_dict.get(realname)

    if request.method == 'POST':
        if form.validate_on_submit():
            work_info = request.form.to_dict()
            # table_titles = ['周', '姓名', '开始日期', '结束日期', '工作类别', '工作内容', '当前状态']
            # return render_template('work_put_succ.html',
            #                        table_titles=table_titles,
            #                        staff_name=staff_name,
            #                        week=week,
            #                        realname=realname,
            #                        start_date=s_date,
            #                        end_date=e_date,
            #                        work_type=w_type,
            #                        content=w_content,
            #                        state=w_state
            #                        )
            return str(work_info)

    return render_template('update_work.html',
                           form=form,
                           staffname=realname
                           )


if __name__ == '__main__':
    app.run(debug=True)
