from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import session
from functools import wraps

engine_user = create_engine("mysql+pymysql://root:a123456@localhost:3306/user?charset=utf8",pool_recycle=7200)
Session_user = sessionmaker(autocommit=False, autoflush=True, bind=engine_user)
session_user = Session_user()

# 登录检验（用户名、密码验证）
def valid_login(username, password):
    global session_user
    user = list(session_user.execute("SELECT * FROM user WHERE username = '{user}' AND password = '{passwd}'".format(
        user = username,
        passwd = password,
        ))
    )
    session_user.close()
    if len(user)>0:
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    global session_user
    user = list(session_user.execute("SELECT * FROM user WHERE username = '{user}' OR email = '{email}'".format(
        user = username,
        email = email,
        ))
    )
    session_user.close()
    if len(user)>0:
        return False
    else:
        return True

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url)) #
    return wrapper