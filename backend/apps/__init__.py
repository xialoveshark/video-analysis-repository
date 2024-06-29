from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session

from exts import db
import settings
import apps.models


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.DevelopmentConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './flask_session/'  # 保存session的文件夹路径
    app.config['SESSION_PERMANENT'] = False  # 确保会话不过期
    Session(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    return app
