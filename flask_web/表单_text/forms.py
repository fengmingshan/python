from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Text_classify(FlaskForm):
    text = TextAreaField('Text Content', validators=[DataRequired(message=("文本内容不能为空！"))],
                         render_kw={'class':'text', 'text-body':'', 'cols':80, 'rows': 4, 'placeholder': u'请输入需要分类的文本。'})
    cutword = TextAreaField('Cut Word', render_kw={'class':'cutword', 'text-body':'', 'cols':80, 'rows': 4, 'placeholder': u'经过分词后的结果。'})
    result = TextAreaField('Classify Result ', render_kw={'class':'result', 'text-body':'', 'cols':80, 'rows': 2, 'placeholder': u'分类结果。'})
    submit = SubmitField('开始分类', render_kw={'class':'submit', 'text-body':'','rows': 2})
