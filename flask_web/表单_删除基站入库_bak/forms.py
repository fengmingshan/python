from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class Delete_bts_form(FlaskForm):
    omc = RadioField('网管名称', choices=[('4', '中兴4G网管'), ('3', '中兴3G网管')])
    type = RadioField('设备类型', choices=[('b', 'BBU'), ('r', 'RRU')])
    btsid = StringField('基站代码', validators=[DataRequired(message=("基站代码不能为空！"))],
                      render_kw={'class': 'info', 'placeholder': u'eNodeB_ID：730100'})
    btsname = StringField('网管基站名称', validators=[DataRequired(message=("网管基站名称不能为空！"))],
                      render_kw={'class': 'info', 'placeholder': u'麒麟寥廓电信办公大楼L8'})
    reason = SelectField('删除原因', choices=[('0', '停电'), ('1', '光缆断'), ('2', '设备故障'), ('3', '站址搬迁'), ('4', '物业纠纷'), ('5', '学校放假'),
                                         ('6', '其他')], render_kw={'class': 'info'})
    shuttime = DateField('删除起止时间',render_kw={'class': 'info', 'placeholder': u'2019-10-31'})
    bbustate = RadioField('BBU是否拆除', choices=[('y', '是'), ('n', '否')])
    rrustate = RadioField('RRU是否拆除', choices=[('y', '是'), ('n', '否')])
    antstate = RadioField('天线是否拆除', choices=[('y', '是'), ('n', '否')])
    submit = SubmitField('提交入库', render_kw={'class': 'info', 'text-body': '', 'rows': 2})
