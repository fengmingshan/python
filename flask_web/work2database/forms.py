from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired 


class Delete_bts_form(FlaskForm):
    omc = RadioField('网管名称', choices=[('中兴4G网管', '中兴4G网管'), ('中兴3G网管', '中兴3G网管')])
    type = RadioField('设备类型', choices=[('BBU', 'BBU'), ('RRU', 'RRU')])
    btsid = StringField('基站代码', render_kw={'class': 'info', 'placeholder': u'eNodeB_ID：730100'})
    btsname = StringField('网管基站名称', render_kw={'class': 'info', 'placeholder': u'麒麟寥廓电信办公大楼L8'})
    reason = SelectField('删除原因', choices=[('0', '停电'), ('1', '光缆断'), ('2', '设备故障'), ('3', '站址搬迁'), ('4', '物业纠纷'), ('5', '学校放假'),
                                         ('6', '其他')], render_kw={'class': 'info'})
    shuttime = DateField('删除起止时间',render_kw={'class': 'info', 'placeholder': u'2019-10-31'})
    bbustate = RadioField('BBU是否拆除', choices=[('是', '是'), ('否', '否')])
    rrustate = RadioField('RRU是否拆除', choices=[('是', '是'), ('否', '否')])
    antstate = RadioField('天线是否拆除', choices=[('是', '是'), ('否', '否')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})


class Complaint_form(FlaskForm):
    serial_number = StringField('工单号码', validators=[DataRequired(message=("工单号不能为空！"))],
                      render_kw={'class': 'info', 'cols': 80, 'placeholder': u'投诉工单号。'})
    content = TextAreaField('投诉内容', validators=[DataRequired(message=("投诉内容不能为空！"))],
                            render_kw={'class': 'info',  'cols': 80, 'rows': 4,
                                       'placeholder': u'用户投诉内容（文本）。'})
    result = TextAreaField('处理结果', validators=[DataRequired(message=("我方处理结果不能为空！"))],
                           render_kw={'class': 'info',  'cols': 80, 'rows': 4,
                                      'placeholder': u'我方处理结果。'})
    country = SelectField('区县', choices=[('未知', '未知'), ('沾益', '沾益'), ('马龙', '马龙'), ('陆良', '陆良'), ('师宗', '师宗'), ('罗平', '罗平'),
                                         ('宣威', '宣威'), ('会泽', '会泽'), ('富源', '富源'), ('麒麟', '麒麟')], render_kw={'class': 'info'})
    town = StringField('乡镇',
                       render_kw={'class': 'info',  'cols': 10, 'rows': 1,
                                  'placeholder': u'投诉工单关联的乡镇。'})
    area = SelectField('区域', choices=[('未知', '未知'), ('城区', '城区'), ('乡镇', '乡镇'), ('农村', '农村')], render_kw={'class': 'info'})
    area_fenlei = SelectField('区域细类', choices=[('未知', '未知'), ('住宅小区', '住宅小区'), ('厂矿企业', '厂矿企业'),
                        ('政府机关单位', '政府机关单位'),('商业区','商业区'),('学校','学校'),('医院','医院'),('宾馆酒店','宾馆酒店'),
                        ('交通枢纽','交通枢纽'),('娱乐场所','娱乐场所'),('乡镇','乡镇'),('自然村','自然村')], render_kw={'class': 'info'})
    village = StringField('自然村/小区',
                          render_kw={'class': 'info', 'cols': 10, 'rows': 1,
                                     'placeholder': u'投诉工单关联的自然村或小区。'})
    lon = StringField('自然村经纬度',
                     render_kw={'class': 'info', 'placeholder': u'g103.xxxx,26.xxxx'})
    res = SelectField('我方办结原因', choices=[('未知', '未知'), ('弱覆盖', '弱覆盖'), ('无覆盖', '无覆盖'), ('基站故障', '基站故障'), ('光缆故障', '光缆故障'), ('用户终端故障', '用户终端故障'),
                                         ('容量问题', '容量问题'), ('优化问题', '优化问题'), ('达量限速', '达量限速'), ('其他', '其他')], render_kw={'class': 'info'})
    measure = SelectField('解决措施',
                      choices=[('未知', '未知'), ('处理基站故障', '处理基站故障'), ('优化调整', '优化调整'), ('基站扩容', '基站扩容'), ('基站建设', '基站建设'), ('使用WIFI替代', '使用WIFI替代'),
                               ('用户自行处理', '用户自行处理'), ('网络正常无需处理', '网络正常无需处理'), ('非本期间故障无法处理', '非本期间故障无法处理'), ('开通volte替代', '开通volte替代')], render_kw={'class': 'info'})
    bts_id = StringField('基站名称',
                         render_kw={'class': 'stringfield', 'placeholder': u'奥维地图基站全名：729601_宣威双龙环东路1.8G_宏站'})
    submit = SubmitField('提交', render_kw={'class': 'info', 'rows': 2})


class Work_report_form(FlaskForm):
    start_date = DateField('开始日期', render_kw={'class': 'info', 'placeholder': u'2020-06-01'})
    end_date = DateField('结束日期', render_kw={'class': 'info', 'placeholder': u'2020-06-30'})
    work_type = SelectField('工作类别', choices=[('例行工作', '例行工作'), ('安排的工作', '安排的工作'),('零时性工作', '零时性工作'), ('专项工作','专项工作'),('主动作为','主动作为'),('微创新', '微创新'), ('学习提升', '学习提升')],
                            render_kw={'class': 'info'})
    content = TextAreaField('工作内容', render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 3,
                                               'placeholder': u'完成XXXXX。'})
    state = RadioField('当前状态', choices=[('已完成', '已完成'), ('进行中', '进行中'), ('待反馈', '待反馈')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})


class Plan_work_form(FlaskForm):
    name = SelectField('姓名', choices=[('王鑫', '王鑫'), ('周朝城', '周朝城'), ('田中玉', '田中玉'), ('解艳刚', '解艳刚'), ('史艳丽', '史艳丽'),
                                      ('查天星', '查天星'), ('冯明山', '冯明山')], render_kw={'class': 'info'})
    start_date = DateField('开始日期', render_kw={'class': 'info', 'placeholder': u'2020-06-01'})
    content = TextAreaField('工作内容', render_kw={'class': 'info', 'cols': 80, 'rows': 3,
                                               'placeholder': u'完成了XXXXX。'})
    submit = SubmitField('提交入库', render_kw={'class': 'info','rows': 2})
