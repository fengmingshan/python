# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 21:26:21 2018
如果写程序用pymysql和程序交互，那就要写原生sql语句。如果进行复杂的查询，那sql语句就要进行一点一点拼接，而且不太有重用性，
扩展不方便。而且写的sql语句可能不高效，导致程序运行也变慢。 为了避免把sql语句写死在代码里，
有没有一种方法直接把原生sql封装好了并且以你熟悉的方式操作，像面向对象那样？ 
orm（object relational mapping）,就是对象映射关系程序， 通过orm将编程语言的对象模型和数据库的关系模型建立映射关系，
这样我们在使用编程语言对数据库进行操作的时候可以直接使用编程语言的对象模型进行操作就可以了，而不用直接使用sql语言。
ORM 相当于把数据库也给你实例化了，在代码操作mysql中级又加了orm这一层。 
@author: Administrator
"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine=create_engine('mysql+pymysql://root:123456@218.63.75.42:3306/test?charset=utf8',echo=False)
DBSession=sessionmaker(bind=engine) 
session=DBSession()

Base = declarative_base()   #生成ORM对象的基类
# 定义User对象:
class User(Base):  #这里的User是ORM对象，user是数据库中的表格，通过定义对象将表user与对象User建立了关联
    # 表的名字:
    __tablename__ = 'user'
    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    password = Column(String(64))
Base.metadata.create_all(engine) #创建表结构 （这里是父类调子类）
session.commit()    #确认修改
session.close()     #关闭会话

#刚才表格已经创建完成了，可以连上数据库看看，
#下面可以在表格中插入记录了
session=DBSession()     #创建session对象，因为刚才的session被关闭了
new_user = User(id='5', name='Bob')     #创建新User对象:
session.add(new_user)
session.commit()
session.close()

#下面看一下怎么查询记录
# 创建Session:
session = DBSession()   #创建session对象,因为刚才的session被关闭了
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one() 
# 打印类型和对象的name属性:
print('type:', type(user))
print('name:', user.name)

'''
#这里还有另外一种创建表的方法
分别创建表和对象，通过mapper()函数建立关联
'''
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

engine=create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8',echo=False)

#创建表
metadata = MetaData()
user = Table('user', metadata,     #定义SQL表格user,这里建立了两个表：一个是表元数据metadata，一个是表结构user
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('password', String(12))
        )

class User(object):     #定义ORM对象User
    def __init__(self, id,name,password):
        self.id = id
        self.name = name
        self.password = password
    def __repr__(self):     #定义查询数据返回的格式，前面加上了字段名，如果不定义该段，查询返回只有值，可读性不好
        return "<User(id='%s',name='%s',  password='%s')>" % (self.id,
        self.name, self.password)
        
mapper(User, user)  #对象User 和 表格user关联起来
Base.metadata.create_all(engine)  #创建表

DBSession=sessionmaker(bind=engine)     #将session实例和engine关联起来。
session=DBSession()     #生成session实例
session.commit()    #确认修改
session.close()     #关闭会话

#往表格中添加元素
DBSession=sessionmaker(bind=engine)     #将session实例和engine关联起来。
session=DBSession()     #生成session实例
user_obj = User(id=27,name="fgf",password="123456")  # 生成你要创建的数据对象

session.add(user_obj)   #在表格中添加元素
session.commit()    #确认修改
session.close()     #关闭会话


'''
查询表格中的元素
'''
session=DBSession()     #生成session实例

my_user = session.query(User).filter_by(name="fgf").first()  # 带条件查询，filter_by就是where条件:name='gfg'。.first()表示返回第一条记录 
print(my_user)  #这里my_user是一个查询结果，被映射成一个对象。所以打印不出来。如果创建表格的时候定义了返回格式，那么返回的内容直接可读
print(my_user.id,my_user.name,my_user.password)     #这样写就能看到内容了

#再增加几条元素，以方便实验
user_obj = User(id=1,name="ztx",password="z444444")  # 生成你要创建的数据对象
user_obj1 = User(id=10,name="gqy",password="x111111")  # 生成你要创建的数据对象
user_obj2 = User(id=30,name="jyg",password="j222222")  # 生成你要创建的数据对象
user_obj3 = User(id=20,name="syl",password="s333333")  # 生成你要创建的数据对象

session.add(user_obj)   #在表格中添加元素
session.add(user_obj1)   #在表格中添加元素
session.add(user_obj2)   #在表格中添加元素
session.add(user_obj3)   #在表格中添加元素

session.commit()    #确认修改

my_user = session.query(User).filter_by().all() #查询全部，.all()就是返回所有记录
print(my_user) 

my_user = session.query(User.name,User.id).all() #查询全部记录返回name，id字段等同于select name，id，.all()就是返回所有记录
print(my_user)     

#.filter与.filter_by
my_user1 = session.query(User).filter(User.id>2).all()
my_user2 = session.query(User).filter_by(id=27).all()  # filter_by相等用‘=’
my_user3 = session.query(User).filter(User.id==28).all()  # filter相等用‘==’
print(my_user1,'\n',my_user2,'\n',my_user3)

#多条件查询
my_user = session.query(User).filter(User.id>0).filter(User.id<20).all()    #两个条件查询
print(my_user)  

my_user = session.query(User).filter(User.id.between(1, 10), User.name == 'gqy').all()  #两个条件查询
print(my_user)  

my_user = session.query(User).filter(User.id.in_([1,10,20])).all()  #id在列表中
print(my_user) 

my_user = session.query(User).filter(~User.id.in_([1,10,20])).all()  #id不在列表中，~表示取反的意思
print(my_user) 

my_user=session.query(User).filter(User.id.in_(session.query(User.id).filter(User.id>20))).all()    #查询嵌套,查询User.id>20的所有记录
print(my_user) 

my_user=session.query(User).filter(User.id.in_(session.query(User.id).filter_by(name='gqy'))).all()   #查询嵌套,查询User.name=‘gqy’的完整记录
print(my_user) 

#多条件查询 and_ 和 or_
from sqlalchemy import and_, or_   #首先要导入and和or函数
ret = session.query(Users).filter(and_(Users.id > 3, Users.name == 'eric')).all()

session.close()     #最后别忘了关闭会话
