from flask import Flask,url_for,render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    dates = ['2020-07-01','2020-07-01','2020-07-01']
    # 对表单信息进行校验，校验失败在模板上追加报错信息
    check = True
    # check = False
    head_info = '<h3>我是顶部的消息</h3>'
    tail_info = '<h3>我是尾部的消息</h3>'
    if check== True:
        return render_template('index.html', head_info = '',tail_info = '', dates=dates)
    else:
        return render_template('index.html', head_info = head_info, tail_info = tail_info, dates=dates)
if __name__ == '__main__':
    app.run()
