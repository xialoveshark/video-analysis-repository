import os


class Config:
    DEBUG = True
    HOSTNAME = 'localhost'
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = '请自己创建数据库，然后替换为数据库的密码'
    DATABASE = 'vsystem'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"


class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'

