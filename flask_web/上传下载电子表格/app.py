# -*- coding: utf-8 -*-
import os
import pandas as pd
import time
import hashlib

from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet,configure_uploads, IMAGES, patch_request_class
from config import Config
from form import UploadForm

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['zip'] = zip


excel_files = set(['xls', 'xlsx', 'csv'])
excels = UploadSet('excels', excel_files)
configure_uploads(app, excels)
patch_request_class(app)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file_obj = request.files.get('excel', '')
        #获得文件名
        file_name = file_obj.filename
        #获得文件格式
        file_postfix = file_name.split('.')[-1]
        #对文件进行重命名
        store_filename = '{}.{}'.format('tmp', file_postfix)
        #检查文件保存路径
        if not os.path.exists(app.config['UPLOADED_EXCELS_DEST']):
            os.makedirs(app.config['UPLOADED_EXCELS_DEST'])

        path = os.path.join(app.config['UPLOADED_EXCELS_DEST'], store_filename)
        #保存文件
        file_obj.save(path)
        success = True
    else:
        success = False
    return render_template('index.html', form=form, success=success)


if __name__ == '__main__':
    app.run()
