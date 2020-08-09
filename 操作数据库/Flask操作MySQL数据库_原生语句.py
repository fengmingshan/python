# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:16:45 2020

@author: Administrator
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine_test = create_engine("mysql+pymysql://root:a123456@218.63.75.43:3306/qjwx_tousu?charset=utf8",pool_recycle=7200)

Session_test = sessionmaker(autocommit=False, autoflush=True, bind=engine_test)

session_test = Session_del()

# =============================================================================
# 查表
# =============================================================================
# 原生数据库语句_推荐
item = db.session.execute('select * from user order by id asc')
# #将结果集强转为list
item = list(item)
for i in item:
    print(i)


# =============================================================================
# 增加内容
# =============================================================================
# 原生SQL语句方式
db.session.execute(r'insert into user values (8, "wjz", "test123")')
db.session.execute(r'insert into user values (9, "ggl", "admin123")')
db.session.commit()

# =============================================================================
# 删除内容
# =============================================================================

# 原生SQL语句方式
db.session.execute(r'delete from user where id = 7')
db.session.commit()

# =============================================================================
# 修改内容
# =============================================================================

# 原生SQL语句方式
db.session.execute(r'update user set name="李四" where id= 4')
db.session.execute(r'update user set name="王二" where id= 5')
db.session.commit()

