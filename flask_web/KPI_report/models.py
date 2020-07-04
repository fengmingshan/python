from exts import db

class Tousu(db.Model):
    #声明表名
    __tablename__ = 'tousu'
    #建立字段函数
    工单流水号 = db.Column(db.String(30),primary_key=True)
    投诉内容 = db.Column(db.String(1024))
    处理结果 = db.Column(db.String(200))
    我方办结原因 = db.Column(db.String(200))
    区县 = db.Column(db.String(200))
    乡镇 = db.Column(db.String(200))
    关联自然村_小区名 = db.Column(db.String(200))
    经度 = db.Column(db.String(200))
    纬度 = db.Column(db.String(200))
    关联基站代码 = db.Column(db.String(200))
    关联基站名称 = db.Column(db.String(200))
    投诉大类 = db.Column(db.String(200))
    投诉原因 = db.Column(db.String(200))
    网络类型 = db.Column(db.String(200))
    区域 = db.Column(db.String(200))
    区域细类 = db.Column(db.String(200))
    解决措施 = db.Column(db.String(200))
    解决措施_详 = db.Column(db.String(200))
    def __repr__(self):
        return '<工单流水号 :{}  投诉内容 :{}	区县 :{}	乡镇 :{}	关联自然村_小区名 :{}	经度 :{}	纬度 :{}	关联基站代码 :{}	关联基站名称 :{}	投诉大类 :{}	投诉原因 :{}	网络类型 :{}	区域 :{}	区域细类 :{}	我方办结原因 :{}	我方办结原因_详 :{}	解决措施 :{}	解决措施_详 :{}>'.format(self.工单流水号 ,	self.投诉类型 ,	self.投诉内容 ,	self.区县 ,	self.乡镇 ,	self.关联自然村_小区名 ,	self.经度 ,	self.纬度 ,	self.关联基站代码 ,	self.关联基站名称 ,	self.投诉大类 ,	self.投诉原因 ,	self.网络类型 ,	self.区域 ,	self.区域细类 ,	self.我方办结原因 ,	self.我方办结原因_详 ,	self.解决措施 ,	self.解决措施_详)

class Rrc_recon(db.Model):
    #声明表名
    __tablename__ = 'rrc_recon'
    #建立字段函数
    TOP小区号 = db.Column(db.String(30),primary_key=True)
    TOP小区名称 = db.Column(db.String(200))
    重建原因 = db.Column(db.String(200))
    处理结果 = db.Column(db.String(200))
    处理详情 = db.Column(db.String(1024))
    def __repr__(self):
        return '<TOP小区号 :{}  TOP小区名称 :{}	重建原因 :{}	处理结果 :{}	处理详情 :{}>'.format(self.TOP小区号 ,	self.TOP小区名称 ,	self.重建原因 ,	self.处理结果 ,	self.处理详情)

class Rrc_rate(db.Model):
    #声明表名
    __tablename__ = 'rrc_rate'
    #建立字段函数
    TOP小区号 = db.Column(db.String(30),primary_key=True)
    TOP小区名称 = db.Column(db.String(200))
    重建原因 = db.Column(db.String(200))
    处理结果 = db.Column(db.String(200))
    处理详情 = db.Column(db.String(1024))
    def __repr__(self):
        return '<TOP小区号 :{}  TOP小区名称 :{}	重建原因 :{}	处理结果 :{}	处理详情 :{}>'.format(self.TOP小区号 ,	self.TOP小区名称 ,	self.重建原因 ,	self.处理结果 ,	self.处理详情)

class Erab_drop(db.Model):
    #声明表名
    __tablename__ = 'erab_drop'
    #建立字段函数
    TOP小区号 = db.Column(db.String(30),primary_key=True)
    TOP小区名称 = db.Column(db.String(200))
    掉线原因 = db.Column(db.String(200))
    处理结果 = db.Column(db.String(200))
    处理详情 = db.Column(db.String(1024))
    def __repr__(self):
        return '<TOP小区号 :{}  TOP小区名称 :{}	掉线原因 :{}	处理结果 :{}	处理详情 :{}>'.format(self.TOP小区号 ,	self.TOP小区名称 ,	self.掉线原因 ,	self.处理结果 ,	self.处理详情)

class Vol_connect(db.Model):
    #声明表名
    __tablename__ = 'vol_connect'
    #建立字段函数
    TOP小区号 = db.Column(db.String(30),primary_key=True)
    TOP小区名称 = db.Column(db.String(200))
    未接通原因 = db.Column(db.String(200))
    处理结果 = db.Column(db.String(200))
    处理详情 = db.Column(db.String(1024))
    def __repr__(self):
        return '<TOP小区号 :{}  TOP小区名称 :{}	未接通原因 :{}	处理结果 :{}	处理详情 :{}>'.format(self.TOP小区号 ,	self.TOP小区名称 ,	self.未接通原因 ,	self.处理结果 ,	self.处理详情)

class Vol_drop(db.Model):
    #声明表名
    __tablename__ = 'vol_drop'
    #建立字段函数
    TOP小区号 = db.Column(db.String(30),primary_key=True)
    TOP小区名称 = db.Column(db.String(200))
    掉话原因 = db.Column(db.String(200))
    处理结果 = db.Column(db.String(200))
    处理详情 = db.Column(db.String(1024))
    def __repr__(self):
        return '<TOP小区号 :{}  TOP小区名称 :{}	掉话原因 :{}	处理结果 :{}	处理详情 :{}>'.format(self.TOP小区号 ,	self.TOP小区名称 ,	self.掉话原因 ,	self.处理结果 ,	self.处理详情)
