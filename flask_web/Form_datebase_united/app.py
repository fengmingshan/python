from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config.from_object('config')

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/first_flask?charset=utf-8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
#建立数据库对象
db = SQLAlchemy(app)

class Traffic(db.Model):
    #声明表名
    __tablename__ = 'traffic'
    #建立字段函数
    enodeb = db.Column(db.Integer,primary_key=True)
    cellid = db.Column(db.Integer(200))
    throughput = db.Column(db.Integer(200))
    def __repr__(self):
        return '<User enodeb: {} cellid: {} throughput: {}>'.format(self.enodeb,self.cellid, self.throughput)
db.create_all()

@app.route('/')
def hello_world():
    return render_template('index.html',item = item, list_item = list_item)

#数据库的查询操作
@app.route('/query')
def select_user():
    # 添加数据
    user1 = User(enodeb=6, cellid='helloflask', throughput='abc123')
    user2 = User(eNodeBID=7, name='wjz', password='test123')
    user3 = User(id=8, name='cxk', password='admin')
    user4 = User(id=9, name='mht', password='passwd')
    user5 = User(id=10, name='mht', password='passwd')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    # 使用ORM映射查询数据
    item = User.query.filter_by(ci = 730111)order_by('id').all()
    #将动态数据传递给模板
    return render_template('show_result.html',item = item, list_item = list_item)

if __name__ == '__main__':
    app.run()
