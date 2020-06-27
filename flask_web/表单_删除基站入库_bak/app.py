from flask import Flask, render_template, request, redirect, url_for
from config import Config
from forms import Delete_bts_form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object(Config)

engine_del = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/delete_bts?charset=utf8", pool_recycle=7200)
Session_del = sessionmaker(autocommit=False, autoflush=True, bind=engine_del)
session_del = Session_del()


@app.route('/', methods=['GET', 'POST'])
def put2datebase():
    # 将表单类实例化
    form = Delete_bts_form()
    form.omc.default = '4'
    form.type.default = 'b'
    form.bbustate.default = 'n'
    form.rrustate.default = 'n'
    form.antstate.default = 'n'
    form.process()
    if request.method == 'POST':
        if form.validate_on_submit():
            delete_bts_info = request.form.to_dict()
            # omc = delete_bts_info.get('omc')
            # type = delete_bts_info.get('type')
            # btsid = delete_bts_info.get('btsid')
            # btsname = delete_bts_info.get('btsname')
            # reason = delete_bts_info.get('reason')
            # shuttime = delete_bts_info.get('shuttime')
            # bbustate = delete_bts_info.get('bbustate')
            # rrustate = delete_bts_info.get('rrustate')
            # antstate = delete_bts_info.get('antstate')
            # session_rrc.execute(
            #     "INSERT INTO  `网管删除的基站`(`omc`, `type`, `btsid`, `btsname`, `reason`, `shuttime`,`bbustate`,`rrustate`,`antstate`) VALUES ({om},{ty},{id},{na},{re},{sh},{bb},{rr},{an},{wek},{enb},{cell},{name})".format(
            #         om=omc, ty=type, id=btsid, na=btsname,re=reason, sh=shuttime, bb=bbustate, rr=rrustate,an=antstate))
            return render_template('put_succ.html', delete_bts_info=delete_bts_info)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
