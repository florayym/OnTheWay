from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_login import LoginManager
from config import config

moment = Moment()
mail = Mail() # mail = Mail(app)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.message'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 添加路由以及出错页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


