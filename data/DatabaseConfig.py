import os
from config import PRODUCTION
basedir = os.path.abspath(os.path.dirname(__file__))

LOCAL_DATABASE_URL = 'sqlite:///Main.db'
# LOCAL_DATABASE_URL = 'postgres://oevaqidctpcmgn:b7b4498465f27c9c4cc3cda45202b0e307de150398e46b3a21097f6918bed295@ec2-3-91-127-228.compute-1.amazonaws.com:5432/d23lm6ck07c3ru'
DATABASE_URL = os.getenv('DATABASE_URL')


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL if PRODUCTION else LOCAL_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
