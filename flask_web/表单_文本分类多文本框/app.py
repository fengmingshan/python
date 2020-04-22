from flask import Flask,render_template,request,flash,redirect,url_for
from config import Config
from forms import Complaint_form

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/',methods=['GET','POST'])
def text_classify():
    #将表单类实例化
    form = Complaint_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(u'分类成功！')
            form.country.data = u'未知'
            return render_template('index.html',form=form)
    return render_template('index.html',form=form)

if __name__ == '__main__':
    app.run()
