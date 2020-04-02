# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:16:45 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/test123?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
#建立数据库对象
db = SQLAlchemy(app)
#db = SQLAlchemy(app, use_native_unicode='utf8')

#建立数据库类，用来映射数据库表,将数据库的模型作为参数传入
class User(db.Model):
    #声明表名
    __tablename__ = 'user'
    #建立字段函数
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    def __repr__(self):
        return '<User ID: {}  用户名：{} 密码：{}>'.format(self.id, self.name, self.password)
db.create_all()

# =============================================================================
# 查表
# =============================================================================

# ORM方式
userlist = User.query.order_by('id').all()
# 使用class User定义好的格式进行print
for user in userlist:
    print(user)

# 自定义格式print
for user in userlist:
    print(user.id,' ',user.name,' ',user.password)


# 原生数据库语句_推荐
item = db.session.execute('select * from user order by id asc')
# #将结果集强转为list
item = list(item)
for i in item:
    print(i)


# =============================================================================
# 增加内容
# =============================================================================

# ORM方式
user1 = User(id = 6, name='helloflask',password='abc123')
user2 = User(id = 7, name='hiworld',password='def456')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

# 原生SQL语句方式
db.session.execute(r'insert into user values (8, "wjz", "test123")')
db.session.execute(r'insert into user values (9, "ggl", "admin123")')

db.session.commit()

# =============================================================================
# 删除内容
# =============================================================================
# ORM方式
User.query.filter_by(id=6).delete()
User.query.filter_by(id=7).delete()
User.query.filter_by(id=8).delete()
User.query.filter_by(id=9).delete()
db.session.commit()

# 原生SQL语句方式
db.session.execute(r'delete from user where id = 7')
db.session.commit()

# =============================================================================
# 修改内容
# =============================================================================
# ORM方式
User.query.filter_by(id=6).update({'name':'张三'})
User.query.filter_by(id=7).update({'name':'李四'})
db.session.commit()

# 原生SQL语句方式
db.session.execute(r'update user set name="李四" where id= 4')
db.session.execute(r'update user set name="王二" where id= 5')
db.session.commit()

userlist1 = User.query.order_by('id').all()
