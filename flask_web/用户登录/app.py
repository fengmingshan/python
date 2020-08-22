from flask import Flask, request, render_template, redirect, url_for, flash, session
from config import Config
from func import valid_login, valid_regist, login_required

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object(Config)

engine_user = create_engine("mysql+pymysql://root:a123456@localhost:3306/user?charset=utf8",pool_recycle=7200)
Session_user = sessionmaker(autocommit=False, autoflush=True, bind=engine_user)
session_user = Session_user()



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', username=session.get('username'))


# 2.登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("成功登录！")
            session['username'] = request.form.get('username')
            return redirect(url_for('home'))
        else:
            error = '错误的用户名或密码！'

    return render_template('login.html', error=error)

# 3.注销
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# 4.注册
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            error = '两次密码不相同！'
        elif valid_regist(request.form['username'], request.form['email']):
            username,password,email= (request.form['username'], request.form['password1'], request.form['email'])
            session_user.execute("INSERT user (username,password,email) VALUES ('{user}','{passwd}','{mail}')".format(
                user = username,
                passwd = password,
                mail = email,
            ))
            session_user.commit()
            session_user.close()
            flash("成功注册！")
            return redirect(url_for('login'))
        else:
            error = '该用户名或邮箱已被注册！'

    return render_template('regist.html', error=error)


# 5.个人中心
@app.route('/person')
@login_required
def person():
    username = session.get('username')
    user = session_user.execute("SELECT * FROM user WHERE username = '{user}'".format(user = username))
    session_user.close()
    return render_template("person.html", user=user)

if __name__ == '__main__':
    app.run(debug=True)
