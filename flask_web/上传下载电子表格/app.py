# -*- coding: utf-8 -*-
import os
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, make_response, send_from_directory
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
        if not os.path.exists(app.config['UPLOADS_DEFAULT_DEST']):
            os.makedirs(app.config['UPLOADS_DEFAULT_DEST'])
        #保存文件
        file_obj.save(app.config['UPLOADS_DEFAULT_DEST']+'/'+store_filename)

        df = pd.read_excel(file_obj)
        cols = df.columns
        success = True
        return render_template('index.html', form=form, success=success, cols=cols)
    else:
        success = False
    return render_template('index.html', form=form, success=success)

@app.route('/down', methods=['GET'])
def download_file():
    path = app.config['UPLOADS_DEFAULT_DEST']
    df = pd.DataFrame({'col1':[1,2,3,4],'col2':[5,6,7,8]})
    with pd.ExcelWriter(path + './download.xlsx' ) as f:
        df.to_excel(f,index = False)
    filename ='download.xlsx'
    response = make_response(
        send_from_directory(path, filename.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

if __name__ == '__main__':
    app.run()
