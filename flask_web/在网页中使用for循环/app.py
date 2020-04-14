from flask import Flask, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@218.63.75.44:3306/mr_report?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

dates = db.session.execute("select distinct date_time from mr_summary where month(date_time)= 4 ")
dates = list(dates)
dates = [str(x[0])[5:] for x in dates]

@app.route('/')
def hello_world():
    return render_template('index.html',dates = dates)

if __name__ == '__main__':
    app.run()
