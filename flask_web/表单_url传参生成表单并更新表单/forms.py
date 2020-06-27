from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired 


class Work_report_form(FlaskForm):
    start_date = DateField('开始日期', render_kw={'class': 'info', 'placeholder': u'2020-06-01'})
    end_date = DateField('结束日期', render_kw={'class': 'info', 'placeholder': u'2020-06-30'})
    work_type = SelectField('工作类别', choices=[('例行工作', '例行工作'), ('安排的工作', '安排的工作'),('零时性工作', '零时性工作'), ('专项工作','专项工作'),('主动作为','主动作为'),('微创新', '微创新'), ('学习提升', '学习提升')],
                            render_kw={'class': 'info'})
    content = TextAreaField('工作内容', render_kw={'class': 'info', 'text-body': '', 'cols': 80, 'rows': 4,
                                               'placeholder': u'完成XXXXX。'})
    state = RadioField('当前状态', choices=[('已完成', '已完成'), ('进行中', '进行中')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})
