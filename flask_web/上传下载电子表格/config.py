import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qjwx-security-code'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOADED_EXCELS_DEST = r'D:\_python\python\flask_web\上传下载电子表格\upload'