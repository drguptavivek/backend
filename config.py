import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))



class BaseConfig:
    DB_NAME = "backend"

class DevConfig(BaseConfig):
    load_dotenv('.env')
    DEBUG = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')


class ProdConfig:
    load_dotenv('.env.production')
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']

    DB_ENGINE = os.environ.get('DB_ENGINE') #mysql+pymysql
    DB_USER= os.environ.get('DB_USER')#root
    DB_PASSWORD= os.environ.get('DB_PASSWORD')#password
    DB_HOST= os.environ.get('DB_HOST') #localhost
    DB_PORT= os.environ.get('DB_PORT')#3306   
    DB_NAME= os.environ.get('DB_NAME')#backend

    DATABASE_URI= DB_ENGINE + '://'+ DB_USER + ':' + DB_PASSWORD + '@'+ DB_HOST + ':' + DB_PORT + '/' + DB_NAME  
    # DATABASE_URI= mysql+pymysql://root:password@localhost:3306/backend
  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
