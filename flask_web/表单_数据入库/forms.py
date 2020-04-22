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
    country = SelectField('区县', choices=[('0', '麒麟'), ('1', '沾益'), ('2', '马龙'), ('3', '陆良'), ('4', '师宗'), ('5', '罗平'),
                                         ('6', '宣威'), ('7', '会泽'), ('8', '富源')], render_kw={'class': 'info'})
    town = StringField('乡镇',
                       render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1,
                                  'placeholder': u'投诉工单关联的乡镇。'})
    village = StringField('自然村/小区',
                          render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1,
                                     'placeholder': u'投诉工单关联的自然村或小区。'})
    lon = StringField('自然村经度',
                     render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1, 'placeholder': u'103.xxxx'})
    lat = StringField('自然村纬度',
                     render_kw={'class': 'info', 'text-body': '', 'cols': 10, 'rows': 1, 'placeholder': u'25.xxxx'})
    bts_id = StringField('基站代码',
                         render_kw={'class': 'info', 'text-body': '', 'rows': 1, 'placeholder': u'投诉工单关联基站代码。'})
    bts_name = StringField('基站名称',
                           render_kw={'class': 'info', 'text-body': '', 'rows': 1, 'placeholder': u'投诉工单关联的基站名称。'})
    submit = SubmitField('提交', render_kw={'class': 'info', 'text-body': '', 'rows': 2})
