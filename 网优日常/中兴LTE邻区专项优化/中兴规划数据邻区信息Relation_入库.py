from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

work_path = r'D:\基站数据库\_中兴规划数据导出\中兴规划数据_2020-06-01'
os.chdir(work_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.43:3306/hand_over?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
# 建立数据库对象
db = SQLAlchemy(app)

df_relation = pd.read_csv('./结果输出/邻接关系_合.csv')
df_external = pd.read_csv('./结果输出/外部邻区.csv')

df_relation = df_relation[['SubNetwork',
    'MEID',
    'CellId',
    'srcENBId',
    'mcc',
    'mnc',
    'eNBId',
    'NCellId',
    'isRemoveAllowed',
    'isHOAllowed',
    'userLabel',
    'shareCover',
    'qofStCell',
    'isAnrCreated',
    'isX2HOAllowed',
    'stateInd',
    'nCelPriority',
    's1DataFwdFlag',
    'cellIndivOffset',
    'coperType',
    'radioMode',
    'overlapCoverage'
]]
df_relation['key'] = df_relation['MEID'].map(str)+ '_' + df_relation['CellId'].map(str) + '-'+ df_relation['eNBId'].map(str)+ '_' + df_relation['NCellId'].map(str)


# 建立数据库类，用来映射到数据库中的表。
class Relation(db.Model):
    # 声明表名
    __tablename__ = 'relation'
    # 建立字段函数
    key = db.Column(db.String(30), primary_key=True)
    SubNetwork = db.Column(db.Integer)
    MEID = db.Column(db.Integer)
    CellId = db.Column(db.Integer)
    srcENBId = db.Column(db.Integer)
    mcc = db.Column(db.Integer)
    mnc = db.Column(db.Integer)
    eNBId = db.Column(db.Integer)
    NCellId = db.Column(db.Integer)
    isRemoveAllowed = db.Column(db.Integer)
    isHOAllowed = db.Column(db.Integer)
    userLabel = db.Column(db.String(200))
    shareCover = db.Column(db.Integer)
    qofStCell = db.Column(db.Integer)
    isAnrCreated = db.Column(db.Integer)
    isX2HOAllowed = db.Column(db.Integer)
    stateInd = db.Column(db.Integer)
    nCelPriority = db.Column(db.Integer)
    s1DataFwdFlag = db.Column(db.Integer)
    cellIndivOffset = db.Column(db.Integer)
    coperType = db.Column(db.Integer)
    radioMode = db.Column(db.String(10))
    overlapCoverage = db.Column(db.Integer)

    def __repr__(self):
        return '<User key: {}, SubNetwork: {}, MEID: {}, CellId: {}, eNBId: {}, NCellId: {}>'.format(
            self.key, self.SubNetwork, self.MEID, self.CellId, self.eNBId, self.NCellId)

db.drop_all()
db.create_all()

# =============================================================================
# 导入Relation数据
# =============================================================================
relation_data = [Relation(
    key = key,
    SubNetwork = SubNetwork,
    MEID = MEID,
    CellId = CellId,
    srcENBId = srcENBId,
    mcc = mcc,
    mnc = mnc,
    eNBId = eNBId,
    NCellId = NCellId,
    isRemoveAllowed = isRemoveAllowed,
    isHOAllowed = isHOAllowed,
    userLabel = userLabel,
    shareCover = shareCover,
    qofStCell = qofStCell,
    isAnrCreated = isAnrCreated,
    isX2HOAllowed = isX2HOAllowed,
    stateInd = stateInd,
    nCelPriority = nCelPriority,
    s1DataFwdFlag = s1DataFwdFlag,
    cellIndivOffset = cellIndivOffset,
    coperType = coperType,
    radioMode = radioMode,
    overlapCoverage = overlapCoverage
) for key, SubNetwork, MEID, CellId, srcENBId, mcc, mnc, eNBId, NCellId, isRemoveAllowed, isHOAllowed, userLabel, shareCover, qofStCell, isAnrCreated, isX2HOAllowed, stateInd, nCelPriority, s1DataFwdFlag, cellIndivOffset, coperType, radioMode, overlapCoverage in zip(
    df_relation['key'],
    df_relation['SubNetwork'],
    df_relation['MEID'],
    df_relation['CellId'],
    df_relation['srcENBId'],
    df_relation['mcc'],
    df_relation['mnc'],
    df_relation['eNBId'],
    df_relation['NCellId'],
    df_relation['isRemoveAllowed'],
    df_relation['isHOAllowed'],
    df_relation['userLabel'],
    df_relation['shareCover'],
    df_relation['qofStCell'],
    df_relation['isAnrCreated'],
    df_relation['isX2HOAllowed'],
    df_relation['stateInd'],
    df_relation['nCelPriority'],
    df_relation['s1DataFwdFlag'],
    df_relation['cellIndivOffset'],
    df_relation['coperType'],
    df_relation['radioMode'],
    df_relation['overlapCoverage']
)]

for item in relation_data:
    db.session.add(item)
db.session.commit()




