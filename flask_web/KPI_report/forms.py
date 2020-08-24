from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


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
                                         ('6', '宣威'), ('7', '会泽'), ('8', '富源'), ('9', '麒麟')], render_kw={'class': 'info'})
    town = StringField('乡镇',
                       render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1,
                                  'placeholder': u'投诉工单关联的乡镇。'})
    area = SelectField('区域', choices=[('0', '未知'), ('1', '城区'), ('2', '乡镇'), ('3', '农村')], render_kw={'class': 'info'})
    area_fenlei = SelectField('区域细类', choices=[('0', '未知'), ('1', '住宅小区'), ('2', '厂矿企业'),
                        ('3', '政府机关单位'),('4','商业区'),('5','学校'),('6','医院'),('7','宾馆酒店'),
                        ('8','交通枢纽'),('9','娱乐场所'),('10','乡镇'),('11','自然村')], render_kw={'class': 'info'})
    village = StringField('自然村/小区',
                          render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1,
                                     'placeholder': u'投诉工单关联的自然村或小区。'})
    lon = StringField('自然村经度',
                     render_kw={'class': 'info', 'text-body': '', 'cols': 6, 'rows': 1, 'placeholder': u'103.xxxx，25.xxxx'})
    res = SelectField('我方办结原因', choices=[('0', '未知'), ('1', '弱覆盖'), ('2', '无覆盖'), ('3', '基站故障'), ('4', '光缆故障'), ('5', '用户终端故障'),
                                         ('6', '容量问题'), ('7', '优化问题'), ('8', '达量限速'), ('9', '其他')], render_kw={'class': 'info'})
    measure = SelectField('解决措施',
                      choices=[('0', '未知'), ('1', '处理基站故障'), ('2', '优化调整'), ('3', '基站扩容'), ('4', '基站建设'), ('5', '使用WIFI替代'),
                               ('6', '用户自行处理'), ('7', '网络正常无需处理'), ('8', '非本期间故障无法处理'), ('9', '开通volte替代')], render_kw={'class': 'info'})

    bts_id = StringField('基站代码',
                         render_kw={'class': 'info', 'text-body': '', 'rows': 1, 'placeholder': u'投诉工单关联基站代码。'})
    bts_name = StringField('基站名称',
                           render_kw={'class': 'info', 'text-body': '', 'rows': 1, 'placeholder': u'投诉工单关联的基站名称。'})
    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})

class Select_form(FlaskForm):
    eNodeB = StringField('eNodeB_ID', validators=[DataRequired(message=("基站号不能为空！"))],
                      render_kw={'class': 'info', 'placeholder': u'eNodeB_ID'})
    cellid = StringField('Cell_ID', validators=[DataRequired(message=("小区不能为空！"))],
                            render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'Cell_ID'})
    month = StringField('月份', validators=[DataRequired(message=("月份不能为空！"))],
                            render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'月份：数字'})
    date = StringField('日期', validators=[DataRequired(message=("日期不能为空！"))],
                            render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'日期：数字'})
    submit = SubmitField('查询', render_kw={'class': 'info', 'text-body': '', 'rows': 2})

class Rrc_recon_form(FlaskForm):
    cause = SelectField('重建原因', choices=[('故障', '故障'), ('覆盖', '覆盖'), ('干扰', '干扰'), ('切换', '切换'), ('重配置失败', '重配置失败')],
                          render_kw={'class': 'info'})
    measure = SelectField('解决措施', choices=[('处理故障', '处理故障'), ('天馈调整', '天馈调整'), ('干扰排查', '干扰排查'),  ('参数调整', '参数调整'), ('基站建设', '基站建设')],
                       render_kw={'class': 'info'})
    handler  = SelectField('处理人', choices=[('冯明山', '冯明山'), ('孙家雄', '孙家雄'), ('王鑫', '王鑫'), ('周朝城', '周朝城'),
                                           ('田中玉', '田中玉'), ('查天星', '查天星'), ('史艳丽', '史艳丽')],
                          render_kw={'class': 'info'})
    result = TextAreaField('处理详情', validators=[DataRequired(message=("详细处理过程不能为空！"))],
                           render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'详细处理过程'})

    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})

class Rrc_rate_form(FlaskForm):
    cause = SelectField('重建原因', choices=[('故障', '故障'), ('覆盖', '覆盖'), ('干扰', '干扰'), ('切换', '切换'), ('重配置失败', '重配置失败')],
                          render_kw={'class': 'info'})
    measure = SelectField('解决措施', choices=[('处理故障', '处理故障'), ('天馈调整', '天馈调整'),('干扰排查', '干扰排查'), ('优化调整', '优化调整'), ('基站建设', '基站建设')],
                       render_kw={'class': 'info'})
    handler = SelectField('处理人', choices=[('冯明山', '冯明山'), ('孙家雄', '孙家雄'), ('王鑫', '王鑫'), ('周朝城', '周朝城'),
                                          ('田中玉', '田中玉'), ('查天星', '查天星'), ('史艳丽', '史艳丽')],
                          render_kw={'class': 'info'})
    result = TextAreaField('处理详情', validators=[DataRequired(message=("详细处理过程不能为空！"))],
                           render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'详细处理过程'})

    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})

class Erab_drop_form(FlaskForm):
    cause = SelectField('重建原因', choices=[('故障', '故障'), ('覆盖', '覆盖'), ('干扰', '干扰'), ('切换', '切换'), ('重配置失败', '重配置失败'), ('小区拥塞', '小区拥塞'),('ENB过载', 'ENB过载'), ('S1链路故障', 'S1链路故障')],
                          render_kw={'class': 'info'})
    measure = SelectField('解决措施', choices=[('处理故障', '处理故障'), ('天馈调整', '天馈调整'),('干扰排查', '干扰排查'), ('优化调整', '优化调整'), ('基站建设', '基站建设'), ('处理传输故障', '处理传输故障')],
                       render_kw={'class': 'info'})
    handler = SelectField('处理人', choices=[('冯明山', '冯明山'), ('孙家雄', '孙家雄'), ('王鑫', '王鑫'), ('周朝城', '周朝城'),
                                          ('田中玉', '田中玉'), ('查天星', '查天星'), ('史艳丽', '史艳丽')],
                          render_kw={'class': 'info'})
    result = TextAreaField('处理详情', validators=[DataRequired(message=("详细处理过程不能为空！"))],
                           render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'详细处理过程'})

    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})

class Vol_connect_form(FlaskForm):
    cause = SelectField('未接通原因', choices=[ ('故障', '故障'), ('覆盖', '覆盖'), ('干扰', '干扰'), ('切换', '切换'), ('参数或软件故障', '参数或软件故障'), ('小区拥塞', '小区拥塞'), ('S1链路故障', 'S1链路故障')],
                          render_kw={'class': 'info'})
    measure = SelectField('解决 措施', choices=[('处理故障', '处理故障'), ('天馈调整', '天馈调整'),('干扰排查', '干扰排查'),  ('优化调整', '优化调整'), ('基站建设', '基站建设'), ('处理传输故障', '处理传输故障')],
                       render_kw={'class': 'info'})
    handler = SelectField('处理人', choices=[('冯明山', '冯明山'), ('孙家雄', '孙家雄'), ('王鑫', '王鑫'), ('周朝城', '周朝城'),
                                          ('田中玉', '田中玉'), ('查天星', '查天星'), ('史艳丽', '史艳丽')],
                          render_kw={'class': 'info'})
    result = TextAreaField('处理详情', validators=[DataRequired(message=("详细处理过程不能为空！"))],
                           render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'详细处理过程'})

    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})

class Vol_drop_form(FlaskForm):
    cause = SelectField('掉话原因', choices=[ ('故障', '故障'), ('覆盖', '覆盖'), ('干扰', '干扰'), ('切换', '切换'), ('参数或软件故障', '参数或软件故障'), ('小区拥塞', '小区拥塞'), ('S1链路故障', 'S1链路故障')],
                          render_kw={'class': 'info'})
    measure = SelectField('解决措施', choices=[('处理故障', '处理故障'), ('天馈调整', '天馈调整'),('干扰排查', '干扰排查'),  ('优化调整', '优化调整'), ('基站建设', '基站建设'), ('处理传输故障', '处理传输故障')],
                       render_kw={'class': 'info'})
    handler = SelectField('处理人', choices=[('冯明山', '冯明山'), ('孙家雄', '孙家雄'), ('王鑫', '王鑫'), ('周朝城', '周朝城'),
                                          ('田中玉', '田中玉'), ('查天星', '查天星'), ('史艳丽', '史艳丽')],
                          render_kw={'class': 'info'})
    result = TextAreaField('处理详情', validators=[DataRequired(message=("详细处理过程不能为空！"))],
                           render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'详细处理过程'})

    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})