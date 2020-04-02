from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/first_flask?charset=utf-8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
#建立数据库对象
db = SQLAlchemy(app)

#建立数据库类，用来映射数据库表,将数据库的模型作为参数传入
class User(db.Model):
    #声明表名
    __tablename__ = 'user'
    #建立字段函数
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    def __repr__(self):
        return '<User id: {} 用户名: {} 密码: {}>'.format(self.id,self.name, self.password)
db.create_all()

#数据库的查询操作
@app.route('/query')
def select_user():
    # 添加数据
    user1 = User(id=6, name='helloflask', password='abc123')
    user2 = User(id=7, name='wjz', password='test123')
    user3 = User(id=8, name='cxk', password='admin')
    user4 = User(id=9, name='mht', password='passwd')
    user5 = User(id=10, name='mht', password='passwd')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)

    # 修改数据数据
    User.query.filter_by(id=2).update({'name': '王二'})
    User.query.filter_by(id=3).update({'name': '张三'})
    User.query.filter_by(id=4).update({'name': '李四'})

    # 删除数据
    User.query.filter_by(id=10).delete()

    # 提交修改
    db.session.commit()

    # 使用ORM映射查询数据
    item = User.query.order_by('id').all()

    # 使用原生的sql语句查询数据
    # item = db.session.execute('select * from user order by id asc')
    # 将结果集强转为list
    list_item = list(item)
    # item = db.session.execute('update user set password = "321321" where id=7')
    #将动态数据传递给模板
    return render_template('show_result.html',item = item, list_item = list_item)


if __name__ == '__main__':
    app.run()
