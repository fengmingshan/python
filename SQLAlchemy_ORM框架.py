# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 22:02:16 2018

@author: Administrator
"""
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()   # 实例化对象的基类

class User(Base):   # 定义User对象，它是Base的子类   
    __tablename__ = 'user'  # 表的名字:
    id = Column(String(20), primary_key=True)     # 表的结构:
    name = Column(String(20))

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test') # 初始化数据库连接:
DBSession = sessionmaker(bind=engine) # 实例化DBSession

# 创建session对象:
session = DBSession()
# 创建新User对象:
new_user = User(id='5', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()

# =============================================================================
# 查询数据库
# =============================================================================
# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()
# 打印类型和对象的name属性:
print('type:', type(user))
print('name:', user.name)
# 关闭Session:
session.close()
