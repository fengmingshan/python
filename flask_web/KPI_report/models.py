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
