from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# function to create the app
def create_app():
    # this command creates the app
    app = Flask(__name__)
    # this is the secret key for the app
    app.config['SECRET_KEY'] = "helloworld"

    # this is the database
    from .views import views
    from .auth import auth
    # this is the database file
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    return app
