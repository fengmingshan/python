from flask import Flask
from form import MultiUploadForm
from flask import url_for, request, session, flash, redirect,render_template
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from config import Config
import uuid
import os
app = Flask(__name__)

app.config.from_object(Config)

app.config['UPLOAD_PATH'] = r'C:\Users\Administrator\Desktop\jpg'
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/up', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        #验证CSRF令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))
        #检查文件是否存在
        if 'photo' not in request.files:
            flash('图片不能为空')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('photo'):
            #检查文件类型
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename ))
                filenames.append(filename)
            else:
                flash('文件类型错误:')
                return redirect(url_for('multi_upload'))
        flash('上传成功!')
        session['filenames'] = filenames
        return '上传成功!'
    return render_template('upload.html', form=form)



if __name__ == '__main__':
    app.run()
