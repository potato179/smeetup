import flask
from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import MetaData
from flask_cors import CORS

api = Api(
    version='1.0',
    title='KSCY_StudyMatchingService',
    prefix='/api',
    contact='',
    contact_email='jimin112688@gmail.com',
    description="게시물, 로그인, 회원가입 API LIST",
)

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    CORS(app)

    api.init_app(app)
    app.config.from_object(config)

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from model import models

    from routes import routes_list
    routes_list(api)

    return app
