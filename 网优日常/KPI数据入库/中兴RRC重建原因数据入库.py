# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:56:54 2020

@author: dboyc
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:16:45 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

work_path = r'C:\Users\Administrator\Desktop\KPI指标'
os.chdir(work_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.43:3306/rrc_reconnect?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True

# 建立数据库对象
db = SQLAlchemy(app)


title =['日期',
    '结束时间',
    '周',
    '子网',
    '子网名称',
    '网元',
    '网元名称',
    '小区号',
    '小区名称',
    '站号',
    '基站名称',
    '产品',
    'RRC连接重建成功率',
    'RRC重建立比例',
    'RRC重建请求数目',
    'RRC重建成功数目',
    'RRC重建失败数目',
    '切换失败触发的RRC重建立请求次数',
    '其它原因触发的RRC重建立请求次数',
    '重配失败触发的RRC重建立请求次数',
    '切换类型的RRC重建立失败数目',
    '重配置类型的RRC重建立失败数目',
    '其它类型的RRC重建立失败数目',
    '切换类型的RRC连接重建立请求次数',
    '切换类型的RRC连接重建立成功次数',
    '切换类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时',
    '切换类型的RRC连接重建立失败次数_失败原因eNB接纳失败',
    '切换类型的RRC连接重建立失败次数_失败原因UE上下文找不到',
    '切换类型的RRC连接重建立失败次数_失败原因再次重建立',
    '切换类型的RRC连接重建立失败次数_其他原因',
    '重配置类型的RRC连接重建立请求次数',
    '重配置类型的RRC连接重建立成功次数',
    '重配置类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时',
    '重配置类型的RRC连接重建立失败次数_失败原因eNB接纳失败',
    '重配置类型RRC连接重建立失败次数_失败原因UE上下文找不到',
    '重配置类型RRC连接重建立失败次数_失败原因再次重建立',
    '重配置类型RRC连接重建立失败次数_其他原因',
    '其它类型的RRC连接重建立请求次数',
    '其它类型的RRC连接重建立成功次数',
    '其它类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时',
    '其它类型的RRC连接重建立失败次数_失败原因eNB接纳失败',
    '其它类型的RRC连接重建立失败次数_失败原因UE上下文找不到',
    '其它类型的RRC连接重建立失败次数_失败原因再次重建立',
    '其它类型的RRC连接重建立失败次数_其他原因'
]

df_rrc = pd.read_csv('./历史性能_RRC重建分析模板_20200601143925.csv',header = 0, names= title, skiprows = 5,encoding = 'gbk')
df_rrc['周'] = df_rrc['日期'].map(lambda x:int(pd.to_datetime(x).strftime("%V"))-1)
df_rrc['key'] = df_rrc['周'].map(str) + '_' + df_rrc['网元'].map(str) + '_' + df_rrc['小区号'].map(str)

df_rrc['RRC连接重建成功率']=df_rrc['RRC连接重建成功率'].str.strip("%").astype(float)/100;
df_rrc['RRC重建立比例']=df_rrc['RRC重建立比例'].str.strip("%").astype(float)/100;
df_rrc = df_rrc[~pd.isnull(df_rrc['站号'])&~pd.isnull(df_rrc['基站名称'])]


class RRC_recon(db.Model):
    # 声明表名
    __tablename__ = 'rrc重建'
    # 建立字段函数
    key=db.Column(db.String(20),primary_key=True)
    日期=db.Column(db.DateTime)
    结束时间=db.Column(db.DateTime)
    周=db.Column(db.Integer)
    子网=db.Column(db.Integer)
    子网名称=db.Column(db.String(20))
    网元=db.Column(db.Integer)
    网元名称=db.Column(db.String(200))
    小区号=db.Column(db.Integer)
    小区名称=db.Column(db.String(200))
    站号=db.Column(db.Integer)
    基站名称=db.Column(db.String(200))
    产品=db.Column(db.String(20))
    RRC连接重建成功率=db.Column(db.Float)
    RRC重建立比例=db.Column(db.Float)
    RRC重建请求数目=db.Column(db.Integer)
    RRC重建成功数目=db.Column(db.Integer)
    RRC重建失败数目=db.Column(db.Integer)
    切换失败触发的RRC重建立请求次数=db.Column(db.Integer)
    其它原因触发的RRC重建立请求次数=db.Column(db.Integer)
    重配失败触发的RRC重建立请求次数=db.Column(db.Integer)
    切换类型的RRC重建立失败数目=db.Column(db.Integer)
    重配置类型的RRC重建立失败数目=db.Column(db.Integer)
    其它类型的RRC重建立失败数目=db.Column(db.Integer)
    切换类型的RRC连接重建立请求次数=db.Column(db.Integer)
    切换类型的RRC连接重建立成功次数=db.Column(db.Integer)
    切换类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时=db.Column(db.Integer)
    切换类型的RRC连接重建立失败次数_失败原因eNB接纳失败=db.Column(db.Integer)
    切换类型的RRC连接重建立失败次数_失败原因UE上下文找不到=db.Column(db.Integer)
    切换类型的RRC连接重建立失败次数_失败原因再次重建立=db.Column(db.Integer)
    切换类型的RRC连接重建立失败次数_其他原因=db.Column(db.Integer)
    重配置类型的RRC连接重建立请求次数=db.Column(db.Integer)
    重配置类型的RRC连接重建立成功次数=db.Column(db.Integer)
    重配置类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时=db.Column(db.Integer)
    重配置类型的RRC连接重建立失败次数_失败原因eNB接纳失败=db.Column(db.Integer)
    重配置类型RRC连接重建立失败次数_失败原因UE上下文找不到=db.Column(db.Integer)
    重配置类型RRC连接重建立失败次数_失败原因再次重建立=db.Column(db.Integer)
    重配置类型RRC连接重建立失败次数_其他原因=db.Column(db.Integer)
    其它类型的RRC连接重建立请求次数=db.Column(db.Integer)
    其它类型的RRC连接重建立成功次数=db.Column(db.Integer)
    其它类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时=db.Column(db.Integer)
    其它类型的RRC连接重建立失败次数_失败原因eNB接纳失败=db.Column(db.Integer)
    其它类型的RRC连接重建立失败次数_失败原因UE上下文找不到=db.Column(db.Integer)
    其它类型的RRC连接重建立失败次数_失败原因再次重建立=db.Column(db.Integer)
    其它类型的RRC连接重建立失败次数_其他原因=db.Column(db.Integer)

    def __repr__(self):
        return '<RRC_recon 日期:{} 结束时间:{} 周:{} 子网:{} 子网名称:{} 网元:{} 网元名称:{} 小区号:{} 小区名称:{} >'.format(self.日期, self.结束时间, self.周, self.子网, self.子网名称, self.网元, self.网元名称, self.小区号, self.小区名称)
db.create_all()
# =============================================================================
# 导入数据
# =============================================================================
traffic_data = [RRC_recon(
    key=key,
    日期=st,
    结束时间=et,
    周=thg,
    子网=sub,
    子网名称=subn,
    网元=neb,
    网元名称=nen,
    小区号=cell,
    小区名称=celln,
    站号=eno,
    基站名称=enon,
    产品=caferc,
    RRC连接重建成功率=cafrll,
    RRC重建立比例=awc,
    RRC重建请求数目=pcr,
    RRC重建成功数目=rcrs,
    RRC重建失败数目=ucdr,
    切换失败触发的RRC重建立请求次数=aedr,
    其它原因触发的RRC重建立请求次数=cuddst,
    重配失败触发的RRC重建立请求次数=cdddst,
    切换类型的RRC重建立失败数目=sssr,
    重配置类型的RRC重建立失败数目=isss,
    其它类型的RRC重建立失败数目=n3g,
    切换类型的RRC连接重建立请求次数=aitqu,
    切换类型的RRC连接重建立成功次数=aitvu,
    切换类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时=aitvd,
    切换类型的RRC连接重建立失败次数_失败原因eNB接纳失败=ufell,
    切换类型的RRC连接重建立失败次数_失败原因UE上下文找不到=dfell,
    切换类型的RRC连接重建立失败次数_失败原因再次重建立=asuplr,
    切换类型的RRC连接重建立失败次数_其他原因=idl,
    重配置类型的RRC连接重建立请求次数=uuop,
    重配置类型的RRC连接重建立成功次数=duop,
    重配置类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时=pdcch,
    重配置类型的RRC连接重建立失败次数_失败原因eNB接纳失败=prach,
    重配置类型RRC连接重建立失败次数_失败原因UE上下文找不到=ncup,
    重配置类型RRC连接重建立失败次数_失败原因再次重建立=pcu,
    重配置类型RRC连接重建立失败次数_其他原因=maxrrc,
    其它类型的RRC连接重建立请求次数=avgrrc,
    其它类型的RRC连接重建立成功次数=avguu,
    其它类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时=avgdu,
    其它类型的RRC连接重建立失败次数_失败原因eNB接纳失败=avgau,
    其它类型的RRC连接重建立失败次数_失败原因UE上下文找不到=maxau,
    其它类型的RRC连接重建立失败次数_失败原因再次重建立=cur,
    其它类型的RRC连接重建立失败次数_其他原因=tddv
 )for key,st,et,thg,sub,subn,neb,nen,cell,celln,eno,enon,caferc,cafrll,awc,pcr,rcrs,ucdr,aedr,cuddst,cdddst,sssr,isss,n3g,aitqu,aitvu,aitvd,ufell,dfell,asuplr,idl,uuop,duop,pdcch,prach,ncup,pcu,maxrrc,avgrrc,avguu,avgdu,avgau,maxau,cur,tddv in zip(
    df_rrc['key'],
    df_rrc['日期'],
    df_rrc['结束时间'],
    df_rrc['周'],
    df_rrc['子网'],
    df_rrc['子网名称'],
    df_rrc['网元'],
    df_rrc['网元名称'],
    df_rrc['小区号'],
    df_rrc['小区名称'],
    df_rrc['站号'],
    df_rrc['基站名称'],
    df_rrc['产品'],
    df_rrc['RRC连接重建成功率'],
    df_rrc['RRC重建立比例'],
    df_rrc['RRC重建请求数目'],
    df_rrc['RRC重建成功数目'],
    df_rrc['RRC重建失败数目'],
    df_rrc['切换失败触发的RRC重建立请求次数'],
    df_rrc['其它原因触发的RRC重建立请求次数'],
    df_rrc['重配失败触发的RRC重建立请求次数'],
    df_rrc['切换类型的RRC重建立失败数目'],
    df_rrc['重配置类型的RRC重建立失败数目'],
    df_rrc['其它类型的RRC重建立失败数目'],
    df_rrc['切换类型的RRC连接重建立请求次数'],
    df_rrc['切换类型的RRC连接重建立成功次数'],
    df_rrc['切换类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时'],
    df_rrc['切换类型的RRC连接重建立失败次数_失败原因eNB接纳失败'],
    df_rrc['切换类型的RRC连接重建立失败次数_失败原因UE上下文找不到'],
    df_rrc['切换类型的RRC连接重建立失败次数_失败原因再次重建立'],
    df_rrc['切换类型的RRC连接重建立失败次数_其他原因'],
    df_rrc['重配置类型的RRC连接重建立请求次数'],
    df_rrc['重配置类型的RRC连接重建立成功次数'],
    df_rrc['重配置类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时'],
    df_rrc['重配置类型的RRC连接重建立失败次数_失败原因eNB接纳失败'],
    df_rrc['重配置类型RRC连接重建立失败次数_失败原因UE上下文找不到'],
    df_rrc['重配置类型RRC连接重建立失败次数_失败原因再次重建立'],
    df_rrc['重配置类型RRC连接重建立失败次数_其他原因'],
    df_rrc['其它类型的RRC连接重建立请求次数'],
    df_rrc['其它类型的RRC连接重建立成功次数'],
    df_rrc['其它类型的RRC连接重建立失败次数_失败原因等待RRC连接重建立完成定时器超时'],
    df_rrc['其它类型的RRC连接重建立失败次数_失败原因eNB接纳失败'],
    df_rrc['其它类型的RRC连接重建立失败次数_失败原因UE上下文找不到'],
    df_rrc['其它类型的RRC连接重建立失败次数_失败原因再次重建立'],
    df_rrc['其它类型的RRC连接重建立失败次数_其他原因']
)]

for item in traffic_data:
    db.session.add(item)
db.session.commit()
