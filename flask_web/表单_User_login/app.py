from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[
                DataRequired(message= u'邮箱不能为空'), Length(1, 64),
                Email(message= u'请输入有效的邮箱地址，比如：username@domain.com')])
    password = PasswordField(u'密码',
                  validators=[DataRequired(message= u'密码不能为空')])
    validcode = PasswordField(u'验证码',
                             validators=[DataRequired(message=u'验证码不能为空')])
    submit = SubmitField(u'登录')

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h3>Hello, {}!</h3>'.format(request.form['email'])
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def user_index():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h3>Hello, {}!</h3>'.format(request.form['email'])
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()