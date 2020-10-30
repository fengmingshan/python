from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    name  = '朱春婷'
    gender = 'fmale'
    age = 20
    interest = 'java'
    workmates = ['陈雪','徐高原','旷显扬']
    return render_template(
        'index.html',
        name = name,
        gender=gender,
        age=age,
        interest=interest,
        workmates=workmates,
    )


if __name__ == '__main__':
    app.run()
