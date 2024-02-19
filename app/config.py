# config.py
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/Cursos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
