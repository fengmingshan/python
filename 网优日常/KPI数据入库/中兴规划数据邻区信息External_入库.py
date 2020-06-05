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

df_external = pd.read_csv('./结果输出/外部邻区.csv')

df_external = df_external[['SubNetwork',
    'MEID',
    'eNBId',
    'ExternalEUtranCellFDD',
    'antPort1',
    'cellLocalId',
    'cellType',
    'mcc',
    'tac',
    'userLabel',
    'earfcnDl',
    'mnc',
    'pci',
    'earfcnUl',
    'addiFreqBand',
    'bandWidthUl',
    'bandWidthDl',
    'freqBandInd'
]]
df_external['key'] = df_external['MEID'].map(str)+ '-' + df_external['eNBId'].map(str)+ '_' + df_external['cellLocalId'].map(str)
df_external['userLabel'][df_external['userLabel'].isnull()] = '未录入'

# 建立数据库类，用来映射到数据库中的表。
class External(db.Model):
    # 声明表名
    __tablename__ = 'external'
    # 建立字段函数
    key = db.Column(db.String(30), primary_key=True)
    SubNetwork = db.Column(db.Integer)
    MEID = db.Column(db.Integer)
    eNBId = db.Column(db.Integer)
    ExternalEUtranCellFDD = db.Column(db.Integer)
    antPort1 = db.Column(db.Integer)
    cellLocalId = db.Column(db.Integer)
    cellType = db.Column(db.Integer)
    mcc = db.Column(db.Integer)
    tac = db.Column(db.Integer)
    userLabel = db.Column(db.String(200))
    earfcnDl = db.Column(db.Integer)
    mnc = db.Column(db.Integer)
    pci = db.Column(db.Integer)
    earfcnUl = db.Column(db.Integer)
    addiFreqBand = db.Column(db.String(50))
    bandWidthUl = db.Column(db.Integer)
    bandWidthDl = db.Column(db.Integer)
    freqBandInd = db.Column(db.Integer)

    def __repr__(self):
        return '<User key: {}, SubNetwork: {}, MEID: {}, ExternalEUtranCellFDD: {}, eNBId: {}, cellLocalId: {}>'.format(
            self.key, self.SubNetwork, self.MEID, self.ExternalEUtranCellFDD, self.eNBId, self.cellLocalId)

db.drop_all()
db.create_all()


# =============================================================================
# 导入External数据
# =============================================================================
external_data = [External(
    key = key,
    SubNetwork = SubNetwork,
    MEID = MEID,
    eNBId = eNBId,
    ExternalEUtranCellFDD = ExternalEUtranCellFDD,
    antPort1 = antPort1,
    cellLocalId = cellLocalId,
    cellType = cellType,
    mcc = mcc,
    tac = tac,
    userLabel = userLabel,
    earfcnDl = earfcnDl,
    mnc = mnc,
    pci = pci,
    earfcnUl = earfcnUl,
    addiFreqBand = addiFreqBand,
    bandWidthUl = bandWidthUl,
    bandWidthDl = bandWidthDl,
    freqBandInd = freqBandInd
) for key, SubNetwork, MEID, eNBId, ExternalEUtranCellFDD, antPort1, cellLocalId, cellType, mcc, tac, userLabel, earfcnDl, mnc, pci, earfcnUl, addiFreqBand, bandWidthUl, bandWidthDl, freqBandInd in zip(
    df_external['key'],
    df_external['SubNetwork'],
    df_external['MEID'],
    df_external['eNBId'],
    df_external['ExternalEUtranCellFDD'],
    df_external['antPort1'],
    df_external['cellLocalId'],
    df_external['cellType'],
    df_external['mcc'],
    df_external['tac'],
    df_external['userLabel'],
    df_external['earfcnDl'],
    df_external['mnc'],
    df_external['pci'],
    df_external['earfcnUl'],
    df_external['addiFreqBand'],
    df_external['bandWidthUl'],
    df_external['bandWidthDl'],
    df_external['freqBandInd']
)]

for item in external_data:
    db.session.add(item)
db.session.commit()


