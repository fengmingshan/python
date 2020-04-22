from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import DataRequired


class Text_classify(FlaskForm):
    serial_number = StringField('工单号码', validators=[DataRequired(message=("工单号不能为空！"))],
                      render_kw={'class': 'serial_number', 'placeholder': u'投诉工单号。'})
    content = TextAreaField('投诉内容', validators=[DataRequired(message=("投诉内容不能为空！"))],
                            render_kw={'class': 'content', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'用户投诉内容（文本）。'})
    result = TextAreaField('处理结果', validators=[DataRequired(message=("我方处理结果不能为空！"))],
                           render_kw={'class': 'result', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'我方处理结果。'})
    country = SelectField('区县', choices=[('0', '麒麟'), ('1', '沾益'), ('2', '马龙'), ('3', '陆良'), ('4', '师宗'), ('5', '罗平'),
                                         ('6', '宣威'), ('7', '会泽'), ('8', '富源')], render_kw={'class': 'country'})
    submit = SubmitField('开始分类', render_kw={'class':'submit', 'text-body':'','rows': 2})
