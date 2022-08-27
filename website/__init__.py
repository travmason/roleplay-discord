from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from .daniel import Bot
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import logging
LOGLEVEL = os.getenv("LOGLEVEL")
logging.basicConfig(level=logging.INFO)

db = SQLAlchemy()
bot = Bot()
DB_NAME = os.getenv("DB_NAME")

def create_app():
    application = app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ibhsfdiug879243*&*&239230hofea7243r6&%^%&^&#'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return application


def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        logging.info('Created database ' + DB_NAME)
