import os

basedir = os.path.abspath(os.path.dirname(__file__))

LOCAL_DATABASE_URL = 'sqlite:///Main.db'
DATABASE_URL = os.getenv('DATABASE_URL')
PRODUCTION = os.getenv('PRODUCTION')


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL if PRODUCTION else LOCAL_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
