import os

# Get application base dir.
_basedir = os.path.abspath(os.path.dirname(__file__))
print _basedir

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'mysecretkeyvalue'
    TEMPLATE_FOLDER = "templates"
    

class DevelopmentConfig(Config):
    DEBUG = True
    RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'dev.db')
    #DATABASE = '/tmp/flaskr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 80
