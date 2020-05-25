from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField,FloatField
from wtforms.validators import DataRequired


class Text_form(FlaskForm):
    content = TextAreaField('文本内容', validators=[DataRequired(message=("文本内容不能为空！"))],
                            render_kw={'class': 'table', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'文本内容'})
    cutword = TextAreaField('分词结果', render_kw={'class': 'table', 'text-body': '', 'cols': 80, 'rows': 4,
                                       'placeholder': u'分词结果。'})
    result = TextAreaField('分类结果', render_kw={'class': 'table', 'text-body': '', 'cols': 80, 'rows': 4,
                                      'placeholder': u'分类结果。'})
    submit = SubmitField('提交', render_kw={'class': 'table', 'text-body': '', 'rows': 2})