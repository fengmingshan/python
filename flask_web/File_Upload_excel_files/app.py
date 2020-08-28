# -*- coding: utf-8 -*-
import os
import pandas as pd
import time
import hashlib

from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'

work_path = 'D:/_python/python/flask_web/File_Upload_excel_files'
os.chdir(work_path)
if not os.path.exists('upload'):
    os.mkdir('upload')
app.config['UPLOADED_EXCELS_DEST'] = os.getcwd().replace('\\','/') + '/upload'

excel_files = set(['xls', 'xlsx', 'csv'])
excels = UploadSet('excels', excel_files)
configure_uploads(app, excels)
patch_request_class(app)  # set maximum file size, default is 16MB




@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('excel'):
            excels.save(filename)
        success = True
    else:
        success = False
    return render_template('index.html', form=form, success=success)


@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_EXCELS_DEST'])
    return render_template('manage.html', files_list=files_list)


@app.route('/open/<filename>')
def open_file(filename):
    file_url = excels.url(filename)
    if filename.split('.')[1] == 'xlsx' or filename.split('.')[1] == 'xls':
        df = pd.read_excel("./upload/" + filename)
    else:
        df = pd.read_csv("./upload/" + filename, engine = 'python', encoding = 'gbk')
    table_html = df.head().to_html(index = False)
    return render_template('browser.html',file_url = file_url, table_html = table_html)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = excels.path(filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))


if __name__ == '__main__':
    app.run(debug=True)