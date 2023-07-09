from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import psycopg2
import os
from dotenv import load_dotenv

# setting up the database
db = SQLAlchemy()
DB_NAME = "database.db"

# setting up the database connection
load_dotenv()

# Retrieve the 'DB_USER' value from the environment variables and store it in the variable DB_USER.
DB_USER = os.getenv('DB_USER')

# Retrieve the 'DB_PASS' value from the environment variables and store it in the variable DB_PASS.
DB_PASS = os.getenv('DB_PASS')

# Retrieve the 'DB_HOST' value from the environment variables and store it in the variable DB_HOST.
DB_HOST = os.getenv('DB_HOST')

# Retrieve the 'DB_PORT' value from the environment variables and store it in the variable DB_PORT.
DB_PORT = os.getenv('DB_PORT')

# Retrieve the 'DB_NAME' value from the environment variables and store it in the variable DB_NAME.
DB_NAME = os.getenv('DB_NAME')


# function to create the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        from . import models
        db.create_all()

    return app
