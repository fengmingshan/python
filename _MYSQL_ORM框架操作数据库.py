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

Base = declarative_base()   #创建对象Base将ORM基类declarative_base()实例化
# 定义User类:
# User类属于子类，从Base对象继承了ORM基类declarative_base()的属性和方法
class User(Base):  #这里的User是ORM对象，user是数据库中的表格，通过定义类将表user与类User建立了关联
    # 表的名字:
    __tablename__ = 'user'
    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    password = Column(String(64))
Base.metadata.create_all(engine) #调用父类Base类中的方法（函数）.create_all创建表结构 
session.commit()    #确认修改
session.close()     #关闭会话

#刚才表格已经创建完成了，可以连上数据库看看，
#下面可以在表格中插入记录了
session=DBSession()     #创建session对象，因为刚才的session被关闭了
new_user = User(id='5', name='Bob')     #创建新对象new_user带有两个参数
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
ORM框架里面比较重要的知识点
另外一种创建表的方法：分别创建表和对象，通过mapper()函数建立关联。
划重点，这种方法简单易用，是经常用到的，需要重点掌握
'''
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8',echo=False)
Base = declarative_base()   #生成ORM对象的基类

#创建表
metadata = MetaData()
user = Table('user', metadata,     #定义SQL表格user,这里建立了两个表：一个是表元数据metadata，一个是表结构user
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('password', String(12))
        )

class User(object):     #定义ORM类User
    def __init__(self, id,name,password):   #定义User类初始化的方法和类的3个属性：id，name，password
        self.id = id
        self.name = name
        self.password = password
    def __repr__(self):     #定义查询数据返回的格式，前面加上了字段名，如果不定义该段，查询返回只有值，可读性不好
        return "<User(id='%s',name='%s',  password='%s')>" % (self.id,
        self.name, self.password)
        
mapper(User, user)  #对象User 和 表格user关联起来
Base.metadata.create_all(engine)  #创建表

'''
操作表格的记录
'''
#添加单个记录
DBSession=sessionmaker(bind=engine)     #创建将DBsession类和数据库engine关联起来。
session=DBSession()     #创建session对象/实例

user_obj = User(id=27,name="fgf",password="123456")  # 生成你要创建的数据对象
session.add(user_obj)   #在表格中添加元素
session.commit()    #确认修改

#批量添加记录
session.add_all([
    User(id=31,name="alex1", password='123abc'),
    User(id=32,name="alex2", password='456def'),
    User(id=33,name="alex3", password='789hij'),
])
session.commit()    #提交修改
session.close()     #关闭会话

#删除表格中的元素
session.query(User).filter(User.id > 30).delete()
session.commit()

#修改表格中的元素
session.query(User).filter(User.id==30).update({"name" : "099"})    #修改id=30的记录，name=099
session.query(User).filter(User.id==30).update({"name" : "wyb"})    #修改id=30的记录，name=wyb
session.query(User).filter(User.id==30).update({User.name: User.name + "099"}, synchronize_session=False)   #名字后面加099
session.query(User).filter(User.id==1).update({"id": User.id + 1}, synchronize_session="evaluate")  #id比原来+1

session.commit()


'''
查询表格中的元素
ORM 指定查询返回数据格式 默认使用query查询返回的结果为一个对象
方法一：#使用for循环遍历列result才能取出name
result = session.query(User).all()
print(result)      #直接print看不到数据，因为默认返回的是一个对象，需要用迭代法遍历才能print
for i in result:
    print(i.name)
方法二：在定义表格的时候使用__repr__定义返回的内容和格式
def __repr__(self):
    output = "(User(id='%s',name='%s',password='%s')" %(self.id,self.name,self.password)
    return output
上面的代码定义了对象的输出格式：User(id=xx,name=xx,password=xx),这样输出的结果直接可读！
划重点了：第二种方法方便直观，代码少，所以尽量使用第二种方法。
'''

session=DBSession()     #创建session对象/实例

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

my_user = session.query(User).filter(and_(User.id > 10, User.name == 'jyg')).all()
print(my_user) 

my_user = session.query(User).filter(or_(User.id < 20, User.name == 'fms')).all()
print(my_user) 

my_user = session.query(User).filter(
    or_(
        User.id < 25,
        and_(User.name == 'syl', User.id > 10),
        User.password=='654321'
    )).all()
print(my_user) 

# 通配符,字符串查询
my_user1 = session.query(User).filter(User.name.like('s%')).all()
my_user2 = session.query(User).filter(~User.name.like('%y%')).all()
print(my_user1,'\n',my_user2) 

# 切片
my_user = session.query(User)[0:2]
print(my_user) 

my_user = session.query(User)[-2:]
print(my_user) 

# 排序
my_user1 = session.query(User).order_by(User.id.desc()).all()  #User.id倒序
my_user2 = session.query(User).order_by(User.name.desc(), User.id.asc()).all() #User.name倒序，并且User.id正序
print(my_user1) 
print(my_user2) 

# 分组
from sqlalchemy.sql import func
my_user = session.query(
            func.max(User.id),
            func.sum(User.id),
            func.min(User.id)).group_by(User.name).all()
print(my_user)


my_user = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.name).having(func.min(User.id)>10).all()
print(my_user)

#连接表_left_jion、right_jion,inner_jion
#为了试验连接表，要先创建其他几个表
from sqlalchemy import ForeignKey #一对多、多对多表需要用到外键，所以需要先导入外键
# 一对多表
class Favor(Base):
    __tablename__ = 'favor'
    nid = Column(Integer, primary_key=True)
    caption = Column(String(50), default='red', unique=True)

class Person(Base):
    __tablename__ = 'person'
    nid = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=True)
    favor_id = Column(Integer, ForeignKey("favor.nid"))

# 多对多表
class ServerToGroup(Base):
    __tablename__ = 'servertogroup'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.id'))
    group_id = Column(Integer, ForeignKey('group.id'))

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    port = Column(Integer, default=22)
    
Base.metadata.create_all(engine)  #创建表    
session.commit()    #确认修改 
#连接表
tab1 = session.query(User, Favor).filter(User.id == Favor.nid).all()
tab2 = session.query(Person).join(Favor).all()
tab3 = session.query(Person).join(Favor, isouter=True).all()

#组合表 union
q1 = session.query(User.name).filter(User.id > 20)
q2 = session.query(Favor.caption).filter(Favor.nid <2)
tab1 = q1.union(q2).all()
print(tab1)

q1 = session.query(User.name).filter(User.id < 10)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
tab2 = q1.union_all(q2).all()
print(tab2)

session.close()     #最后别忘了关闭会话

'''
ORM 一对多具体使用
mysql表中一对多指的是表A中的数据和表B中的数据存在对应的映射关系，表A中的数据在表B中对应存在多个对应关系，
如表A存放用户的角色 DBA，SA，表B中存放用户，表B通过外键关联表A，多个用户可以属于同一个角色
设计两张表，user表和role表，user 表中存放用户，role表中存放用户角色，role表中角色对应user表中多个用户，
user表中一个用户只对应role表中一个角色，中间通过外键约束
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine

engine=create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8',echo=False)
Base = declarative_base()   #生成ORM对象的基类

class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {"useexisting": True}  #如果已存在就直接使用
    rid = Column(Integer, primary_key=True, autoincrement=True)    #主键，自增
    role_name = Column(String(10))
    def __repr__(self):
        output = "Role(rid='%s',role_name='%s')" %(self.rid,self.role_name)
        return output
    
class Userinfo(Base):
    __tablename__ = 'userinfo'
    __table_args__ = {"useexisting": True}      #如果已存在就直接使用
    nid = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(10),nullable=False)
    role = Column(Integer,ForeignKey('role.rid'))  #外键关联
    group = relationship('Role',backref='uuu')    #建立relationship，Role为类名
    def __repr__(self):
        output = " Userinfo(nid='%s',name='%s',role='%s')" %(self.nid,self.name,self.role)
        return output
Base.metadata.create_all(engine)

DBsession = sessionmaker(bind=engine)
session = DBsession()

session.add(Role(role_name='dba'))
session.add(Role(role_name='sa'))
session.add(Role(role_name='net'))

session.add_all([   #注意因为这里的role被定义成外键，并与role.rid关联，所以如果role.rid没有的值在userinfo表中就会创建失败
    Userinfo(name='fuzj',role='4'),
    Userinfo(name='jie',role='6'),
    Userinfo(name='张三',role='6'),
    Userinfo(name='李四',role='4'),
    Userinfo(name='王五',role='5'),
])
session.commit()

#普通连表查询
res = session.query(Userinfo,Role).join(Role).all()    #查询所有用户,及对应的role id
print(res)

res1 = session.query(Userinfo.name,Role.role_name).join(Role).all()  #查询所有用户名和角色,
print(res1)

res2 = session.query(Userinfo.name,Role.role_name).join(Role,isouter=True).filter(Role.role_name=='dba').all() #查询所有dba的用户
print(res2)

#使用relationship 添加影射关系进行查询
#首先在Userinfo表中添加relationship影射关系
class Userinfo(Base):
    __tablename__ = 'userinfo'
    nid = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(10),nullable=False)
    role = Column(Integer,ForeignKey('role.rid'))
    group = relationship("Role",backref='uuu')    #Role为类名
#relationship 在user表中创建了新的字段，这个字段只用来存放user表中和role表中的对应关系，在数据库中并不实际存在

#正向查询：
res = session.query(Userinfo).all()  #查询所有的用户和角色
for i in res:
    print(i.name,i.group.role_name)    #此时的i.group 就是role表对应的关系
    
res1 = session.query(Userinfo).filter(Userinfo.name=='fuzj').first()  #查询fuzj用户和角色
print(res1.name,res1.group.role_name)
#正向查找： 先从user表中查到符合name的用户之后，此时结果中已经存在和role表中的对应关系，
#group对象即role表，所以直接使用obj.group.role_name就可以取出对应的角色

#反向查询：
res = session.query(Role).filter(Role.role_name =='dba').first()   #查找dba组下的所有用户
print(res.uuu)  
for i in res.uuu:
    print(i.name,res.role_name)
#反向查找：relationship参数中backref='uuu'，会在role表中的每个字段中加入uuu，而uuu对应的就是本字段在user表中对应的所有用户，所以，obj.uuu.name会取出来用户名
#所谓正向和反向查找是对于relationship关系映射所在的表而说，如果通过该表（user表）去查找对应的关系表（role表），就是正向查找.
#反之通过对应的关系表（role表）去查找该表（user表）即为反向查找。而relationship往往会和ForeignKey共存在一个表中。