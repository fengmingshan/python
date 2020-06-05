# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:16:45 2020

@author: Administrator
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from math import ceil
work_path = r'C:\Users\Administrator\Desktop\KPI指标'
os.chdir(work_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.43:3306/hand_over?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True

# 建立数据库对象
db = SQLAlchemy(app)
file_name = '邻区切换分析（20200511-20200517）.csv'

def read_csv_partly(file):
    file_data = pd.read_csv(file, header=0,names= title, encoding = 'gbk', chunksize=50000)
    for df_tmp in file_data:
        yield df_tmp

list_df_ho = read_csv_partly('./'+ file_name)

title =['序号',
    '开始时间',
    '结束时间',
    '周',
    '子网',
    '子网名称',
    '网元',
    '网元名称',
    '小区',
    '小区名称',
    'eNodeB',
    'eNodeB名称',
    '邻区关系',
    '产品',
    '切换出请求总次数',
    '切换入请求总次数',
    '切换出成功次数',
    '切换入成功次数',
    '邻区漏配',
    '切换出成功率',
    '切换入成功率',
    '切换出执行失败次数_源侧发生重建立',
    '切换出执行失败次数_等待UECONTEXTRELEASE消息超时',
    '切换出执行失败次数_其它原因',
    '切换入执行失败次数_RRC重配完成超时',
    '切换入执行失败次数_源侧取消切换',
    '切换入执行失败次数_其他原因',
    '切换入执行失败次数_目标侧发生重建立',
    '切换入准备成功次数',
    '切换入准备失败次数_资源分配失败',
    '切换入准备失败次数_源侧取消切换',
    '切换入准备失败次数_其它原因',
    '切换入准备失败次数_目标侧发生重建立',
    '切换入准备失败次数_传输资源受限',
    '切换出准备成功次数',
    '切换出准备失败次数_等待切换响应定时器超时',
    '切换出准备失败次数_目标侧准备失败',
    '切换出准备失败次数_其它原因',
    '切换出准备失败次数_源侧发生重建立',
    '切换出准备失败次数_用户未激活',
    '切换出准备失败次数_传输资源受限'
]

class Nei_handover(db.Model):
    # 声明表名
    __tablename__ = '邻区切换'
    # 建立字段函数
    key=db.Column(db.String(50),primary_key=True)
    开始时间=db.Column(db.DateTime)
    结束时间=db.Column(db.DateTime)
    周=db.Column(db.Integer)
    子网=db.Column(db.Integer)
    子网名称=db.Column(db.String(50))
    网元=db.Column(db.Integer)
    网元名称=db.Column(db.String(200))
    小区=db.Column(db.Integer)
    小区名称=db.Column(db.String(200))
    eNodeB=db.Column(db.Integer)
    eNodeB名称=db.Column(db.String(200))
    邻区=db.Column(db.String(20))
    邻区关系=db.Column(db.String(50))
    产品=db.Column(db.String(20))
    切换出请求总次数=db.Column(db.BIGINT)
    切换入请求总次数=db.Column(db.BIGINT)
    切换出成功次数=db.Column(db.BIGINT)
    切换出失败次数=db.Column(db.BIGINT)
    切换入成功次数=db.Column(db.BIGINT)
    切换入失败次数=db.Column(db.BIGINT)
    邻区漏配=db.Column(db.BIGINT)
    切换出成功率=db.Column(db.BIGINT)
    切换出执行失败次数=db.Column(db.BIGINT)
    切换出准备失败次数=db.Column(db.BIGINT)
    切换入成功率=db.Column(db.BIGINT)
    切换入执行失败次数=db.Column(db.BIGINT)
    切换入准备失败次数=db.Column(db.BIGINT)
    切换出执行失败次数_源侧发生重建立=db.Column(db.BIGINT)
    切换出执行失败次数_等待UECONTEXTRELEASE消息超时=db.Column(db.BIGINT)
    切换出执行失败次数_其它原因=db.Column(db.BIGINT)
    切换入执行失败次数_RRC重配完成超时=db.Column(db.BIGINT)
    切换入执行失败次数_源侧取消切换=db.Column(db.BIGINT)
    切换入执行失败次数_其他原因=db.Column(db.BIGINT)
    切换入执行失败次数_目标侧发生重建立=db.Column(db.BIGINT)
    切换入准备成功次数=db.Column(db.BIGINT)
    切换入准备失败次数_资源分配失败=db.Column(db.BIGINT)
    切换入准备失败次数_源侧取消切换=db.Column(db.BIGINT)
    切换入准备失败次数_其它原因=db.Column(db.BIGINT)
    切换入准备失败次数_目标侧发生重建立=db.Column(db.BIGINT)
    切换入准备失败次数_传输资源受限=db.Column(db.BIGINT)
    切换出准备成功次数=db.Column(db.BIGINT)
    切换出准备失败次数_等待切换响应定时器超时=db.Column(db.BIGINT)
    切换出准备失败次数_目标侧准备失败=db.Column(db.BIGINT)
    切换出准备失败次数_其它原因=db.Column(db.BIGINT)
    切换出准备失败次数_源侧发生重建立=db.Column(db.BIGINT)
    切换出准备失败次数_用户未激活=db.Column(db.BIGINT)
    切换出准备失败次数_传输资源受限=db.Column(db.BIGINT)

    def __repr__(self):
        return '<User key:{} 开始时间:{} 结束时间:{} 周:{} 子网:{} 子网名称:{} 网元:{} 网元名称:{} 小区:{} 小区名称:{}>'.format(self.key,self.日期,self.结束时间,self.周,self.子网,self.子网名称,self.网元,self.网元名称,self.小区,self.小区名称)
db.drop_all()
db.create_all()


for i,df_ho in enumerate(list_df_ho):
    df_ho['邻区关系']=df_ho['邻区关系'].map(lambda x:'_'.join(x.split(':')[-2:]))
    df_ho['邻区关系']=df_ho['网元'].map(str)+'_'+df_ho['小区'].map(str)+'-'+df_ho['邻区关系'].map(str)
    df_ho['邻区']=df_ho['邻区关系'].map(lambda x:x.split('-')[1])
    #df1= df_ho.head(10)
    df_ho['切换出失败次数']=df_ho['切换出请求总次数']-df_ho['切换出成功次数']
    df_ho['切换入失败次数']=df_ho['切换入请求总次数']-df_ho['切换入成功次数']


    df_ho['切换出执行失败次数']=df_ho['切换出执行失败次数_源侧发生重建立']+df_ho['切换出执行失败次数_等待UECONTEXTRELEASE消息超时']+df_ho['切换出执行失败次数_其它原因']
    df_ho['切换出准备失败次数']=df_ho['切换出准备失败次数_等待切换响应定时器超时']+df_ho['切换出准备失败次数_目标侧准备失败']+df_ho['切换出准备失败次数_其它原因']+df_ho['切换出准备失败次数_源侧发生重建立']+df_ho['切换出准备失败次数_用户未激活']+df_ho['切换出准备失败次数_传输资源受限']
    df_ho['切换入执行失败次数']=df_ho['切换入执行失败次数_RRC重配完成超时']+df_ho['切换入执行失败次数_源侧取消切换']+df_ho['切换入执行失败次数_其他原因']+df_ho['切换入执行失败次数_目标侧发生重建立']
    df_ho['切换入准备失败次数']=df_ho['切换入准备失败次数_资源分配失败']+df_ho['切换入准备失败次数_源侧取消切换']+df_ho['切换入准备失败次数_其它原因']+df_ho['切换入准备失败次数_目标侧发生重建立']+df_ho['切换入准备失败次数_传输资源受限']
    df_ho['周'] = df_ho['开始时间'].map(lambda x:int(pd.to_datetime(x).isocalendar()[1]))
    df_ho['key'] = df_ho['周'].map(str) + '_' + df_ho['邻区关系'].map(str)

    df_ho['切换出成功率']=df_ho['切换出成功率'].str.strip("%").astype(float)/100;
    df_ho['切换入成功率']=df_ho['切换入成功率'].str.strip("%").astype(float)/100;
    df_ho = df_ho[~pd.isnull(df_ho['eNodeB'])&~pd.isnull(df_ho['eNodeB名称'])]

    keys = db.session.execute(r"SELECT `key` from `邻区切换`")
    keys = list(keys)
    keys = [x.key for x in keys]

    df_ho = df_ho[~df_ho['key'].isin(keys) ]


# =============================================================================
# 数据入库
# =============================================================================
    handover_data = [Nei_handover(
        key=key,
        开始时间=st,
        结束时间=et,
        周=thg,
        子网=sub,
        子网名称=subn,
        网元=neb,
        网元名称=nen,
        小区=cell,
        小区名称=celln,
        eNodeB=eno,
        eNodeB名称=enon,
        邻区=lq,
        邻区关系=caferc,
        产品=cafrll,
        切换出请求总次数=awc,
        切换入请求总次数=pcr,
        切换出成功次数=rcrs,
        切换出失败次数=hoou,
        切换入成功次数=ucdr,
        切换入失败次数=hoin,
        邻区漏配=aedr,
        切换出成功率=cuddst,
        切换出执行失败次数=hdou,
        切换出准备失败次数=hrou,
        切换入成功率=cdddst,
        切换入执行失败次数=hdin,
        切换入准备失败次数=hrin,
        切换出执行失败次数_源侧发生重建立=sssr,
        切换出执行失败次数_等待UECONTEXTRELEASE消息超时=isss,
        切换出执行失败次数_其它原因=n3g,
        切换入执行失败次数_RRC重配完成超时=aitqu,
        切换入执行失败次数_源侧取消切换=aitvu,
        切换入执行失败次数_其他原因=aitvd,
        切换入执行失败次数_目标侧发生重建立=ufell,
        切换入准备成功次数=dfell,
        切换入准备失败次数_资源分配失败=asuplr,
        切换入准备失败次数_源侧取消切换=idl,
        切换入准备失败次数_其它原因=uuop,
        切换入准备失败次数_目标侧发生重建立=docs,
        切换入准备失败次数_传输资源受限=duop,
        切换出准备成功次数=pdcch,
        切换出准备失败次数_等待切换响应定时器超时=prach,
        切换出准备失败次数_目标侧准备失败=ncup,
        切换出准备失败次数_其它原因=pcu,
        切换出准备失败次数_源侧发生重建立=maxrrc,
        切换出准备失败次数_用户未激活=avgrrc,
        切换出准备失败次数_传输资源受限=avguu,
     )for key,st,et,thg,sub,subn,neb,nen,cell,celln,eno,enon,lq,caferc,cafrll,awc,pcr,rcrs,hoou,ucdr,hoin,aedr,cuddst,hdou,hrou,cdddst,hdin,hrin,sssr,isss,n3g,aitqu,aitvu,aitvd,ufell,dfell,asuplr,idl,uuop,docs,duop,pdcch,prach,ncup,pcu,maxrrc,avgrrc,avguu in zip(
        df_ho['key'],
        df_ho['开始时间'],
        df_ho['结束时间'],
        df_ho['周'],
        df_ho['子网'],
        df_ho['子网名称'],
        df_ho['网元'],
        df_ho['网元名称'],
        df_ho['小区'],
        df_ho['小区名称'],
        df_ho['eNodeB'],
        df_ho['eNodeB名称'],
        df_ho['邻区'],
        df_ho['邻区关系'],
        df_ho['产品'],
        df_ho['切换出请求总次数'],
        df_ho['切换入请求总次数'],
        df_ho['切换出成功次数'],
        df_ho['切换出失败次数'],
        df_ho['切换入成功次数'],
        df_ho['切换入失败次数'],
        df_ho['邻区漏配'],
        df_ho['切换出成功率'],
        df_ho['切换出执行失败次数'],
        df_ho['切换出准备失败次数'],
        df_ho['切换入成功率'],
        df_ho['切换入执行失败次数'],
        df_ho['切换入准备失败次数'],
        df_ho['切换出执行失败次数_源侧发生重建立'],
        df_ho['切换出执行失败次数_等待UECONTEXTRELEASE消息超时'],
        df_ho['切换出执行失败次数_其它原因'],
        df_ho['切换入执行失败次数_RRC重配完成超时'],
        df_ho['切换入执行失败次数_源侧取消切换'],
        df_ho['切换入执行失败次数_其他原因'],
        df_ho['切换入执行失败次数_目标侧发生重建立'],
        df_ho['切换入准备成功次数'],
        df_ho['切换入准备失败次数_资源分配失败'],
        df_ho['切换入准备失败次数_源侧取消切换'],
        df_ho['切换入准备失败次数_其它原因'],
        df_ho['切换入准备失败次数_目标侧发生重建立'],
        df_ho['切换入准备失败次数_传输资源受限'],
        df_ho['切换出准备成功次数'],
        df_ho['切换出准备失败次数_等待切换响应定时器超时'],
        df_ho['切换出准备失败次数_目标侧准备失败'],
        df_ho['切换出准备失败次数_其它原因'],
        df_ho['切换出准备失败次数_源侧发生重建立'],
        df_ho['切换出准备失败次数_用户未激活'],
        df_ho['切换出准备失败次数_传输资源受限']
    )]

    for item in handover_data:
        db.session.add(item)
    db.session.commit()
    print('已入库： {}W 条记录'.format((i+1)*5))

#db.session.rollback()