from flask import Flask 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Resource, Api
app=Flask(__name__)
app.permanent_session_lifetime=timedelta(minutes=5)
DB_NAME = "database.db"
app.config['SECRET_KEY'] ='07fb3c3e9c4a6be547e5a6ba'
app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
db=SQLAlchemy(app)
api = Api(app)
login_manager.login_view = "app.Login"
login_manager.login_message_category = "info"
login_manager.init_app(app)
from app import routes
