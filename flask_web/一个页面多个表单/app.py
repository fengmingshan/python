# -*- coding: utf-8 -*-
from flask import Flask, render_template
from config import Config
from forms import Form1, Form2

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['zip'] = zip

@app.route('/', methods=['GET', 'POST'])
def multi_form():
    form1 = Form1()
    form2 = Form2()

    if form1.submit1.data and form1.validate_on_submit():
        return 'form1 is being submit'

    if form2.submit2.data and form2.validate_on_submit():
        return 'form2 is being submit'

    return render_template('index.html', form1 = form1,form2 = form2)

if __name__ == '__main__':
    app.run()
