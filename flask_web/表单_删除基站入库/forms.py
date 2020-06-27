from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class Delete_bts_form(FlaskForm):
    omc = RadioField('网管名称', choices=[('中兴4G网管', '中兴4G网管'), ('中兴3G网管', '中兴3G网管')])
    type = RadioField('设备类型', choices=[('BBU', 'BBU'), ('RRU', 'RRU')])
    btsid = StringField('基站代码', render_kw={'class': 'info', 'placeholder': u'eNodeB_ID：730100'})
    btsname = StringField('网管基站名称', render_kw={'class': 'info', 'placeholder': u'麒麟寥廓电信办公大楼L8'})
    reason = SelectField('删除原因',
                         choices=[('0', '停电'), ('1', '光缆断'), ('2', '设备故障'), ('3', '站址搬迁'), ('4', '物业纠纷'), ('5', '学校放假'),
                                  ('6', '其他')], render_kw={'class': 'info'})
    shuttime = DateField('删除起止时间', render_kw={'class': 'info', 'placeholder': u'2019-10-31'})
    bbustate = RadioField('BBU是否拆除', choices=[('是', '是'), ('否', '否')])
    rrustate = RadioField('RRU是否拆除', choices=[('是', '是'), ('否', '否')])
    antstate = RadioField('天线是否拆除', choices=[('是', '是'), ('否', '否')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})


class Complaint_form(FlaskForm):
    serial_number = StringField('工单号码', validators=[DataRequired(message=("工单号不能为空！"))],
                                render_kw={'class': 'info', 'placeholder': u'投诉工单号。'})
    content = TextAreaField('投诉内容', validators=[DataRequired(message=("投诉内容不能为空！"))],
                            render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'用户投诉内容（文本）。'})
    result = TextAreaField('处理结果', validators=[DataRequired(message=("我方处理结果不能为空！"))],
                           render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'我方处理结果。'})
    country = SelectField('区县', choices=[('0', '未知'), ('1', '沾益'), ('2', '马龙'), ('3', '陆良'), ('4', '师宗'), ('5', '罗平'),
                                         ('6', '宣威'), ('7', '会泽'), ('8', '富源'), ('9', '麒麟')],
                          render_kw={'class': 'info'})
    town = StringField('乡镇',
                       render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1,
                                  'placeholder': u'投诉工单关联的乡镇。'})
    area = SelectField('区域', choices=[('0', '未知'), ('1', '城区'), ('2', '乡镇'), ('3', '农村')], render_kw={'class': 'info'})
    area_fenlei = SelectField('区域细类', choices=[('0', '未知'), ('1', '住宅小区'), ('2', '厂矿企业'),
                                               ('3', '政府机关单位'), ('4', '商业区'), ('5', '学校'), ('6', '医院'), ('7', '宾馆酒店'),
                                               ('8', '交通枢纽'), ('9', '娱乐场所'), ('10', '乡镇'), ('11', '自然村')],
                              render_kw={'class': 'info'})
    village = StringField('自然村/小区',
                          render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1,
                                     'placeholder': u'投诉工单关联的自然村或小区。'})
    lon = StringField('自然村经度',
                      render_kw={'class': 'info', 'text-body': '', 'cols': 6, 'rows': 1, 'placeholder': u'103.xxxx'})
    lat = StringField('自然村纬度',
                      render_kw={'class': 'info', 'text-body': '', 'cols': 6, 'rows': 1, 'placeholder': u'25.xxxx'})
    res = SelectField('我方办结原因',
                      choices=[('0', '未知'), ('1', '弱覆盖'), ('2', '无覆盖'), ('3', '基站故障'), ('4', '光缆故障'), ('5', '用户终端故障'),
                               ('6', '容量问题'), ('7', '优化问题'), ('8', '达量限速'), ('9', '其他')], render_kw={'class': 'info'})
    measure = SelectField('解决措施',
                          choices=[('0', '未知'), ('1', '处理基站故障'), ('2', '优化调整'), ('3', '基站扩容'), ('4', '基站建设'),
                                   ('5', '使用WIFI替代'),
                                   ('6', '用户自行处理'), ('7', '网络正常无需处理'), ('8', '非本期间故障无法处理'), ('9', '开通volte替代')],
                          render_kw={'class': 'info'})

    bts_id = StringField('基站代码',
                         render_kw={'class': 'info', 'text-body': '', 'rows': 1, 'placeholder': u'投诉工单关联基站代码。'})
    bts_name = StringField('基站名称',
                           render_kw={'class': 'info', 'text-body': '', 'rows': 1, 'placeholder': u'投诉工单关联的基站名称。'})
    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})


class Work_report_form(FlaskForm):
    start_date = DateField('开始日期', render_kw={'class': 'info', 'placeholder': u'2020-06-01'})
    end_date = DateField('结束日期', render_kw={'class': 'info', 'placeholder': u'2020-06-30'})
    work_type = SelectField('工作类别', choices=[('例行工作', '例行工作'), ('零时性工作', '零时性工作'), ('专项工作','专项工作'),('主动作为','主动作为'),('微创新', '微创新'), ('学习提升', '学习提升')],
                            render_kw={'class': 'info'})
    content = TextAreaField('工作内容', render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                               'placeholder': u'完成XXXXX。'})
    state = RadioField('当前状态', choices=[('已完成', '已完成'), ('进行中', '进行中')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})


class Department_work_report_form(FlaskForm):
    week = IntegerField('周', render_kw={'class': 'info', 'placeholder': u'24'})
    name = SelectField('姓名', choices=[('王鑫', '王鑫'), ('周朝成', '周朝成'), ('田中玉', '田中玉'), ('解艳刚', '解艳刚'), ('史艳丽', '史艳丽'),
                                      ('查天星', '查天星'), ('冯明山', '冯明山')], render_kw={'class': 'info'})
    start_date = DateField('开始日期', render_kw={'class': 'info', 'placeholder': u'2020-06-01'})
    end_date = DateField('结束日期', render_kw={'class': 'info', 'placeholder': u'2020-06-30'})
    work_type = SelectField('工作类别', choices=[('例行工作', '例行工作'), ('零时性工作', '零时性工作'), ('专项工作','专项工作'),('主动作为','主动作为'),('微创新', '微创新'), ('学习提升', '学习提升')],
                            render_kw={'class': 'info'})
    content = TextAreaField('工作内容', render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                               'placeholder': u'完成XXXXX。'})
    state = RadioField('当前状态', choices=[('已完成', '已完成'), ('进行中', '进行中')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})
