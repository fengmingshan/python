import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qjwx-security-code'
    DEBUG = True