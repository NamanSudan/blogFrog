from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# setting up the database
db = SQLAlchemy()
DB_NAME = "database.db"

# function to create the app
def create_app():
    # this command creates the app
    app = Flask(__name__)
    # this is the secret key for the app
    app.config['SECRET_KEY'] = "helloworld"
    # this is the database path
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # this is the database initialization
    db.init_app(app)

    # this is the database
    from .views import views
    # this is the authentication
    from .auth import auth

    # this is the database file
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # importing the User model from models.py
    from .models import User

    # calling the create_database function
    create_database(app)

    # this is the login manager
    login_manager = LoginManager()
    # redirect a user that's not signed-in but wants to access a page that requires a user to be signed-in to the sign-in page
    login_manager.login_view = "auth.sign_in"
    # we pass in the app
    login_manager.init_app(app)

    # function to help login manager to find the user model when it logs something in
    # login manager will uses a session to determine if the user is logged in or not
    @login_manager.user_loader
    # this function will load the user given an id
    def load_user(id):
        # this will return the user with the id
        return User.query.get(int(id))

    return app

def create_database(app):
    # if the database does not exist then create it
    # if the path does not exist then create it
    if not path.exists('website/' + DB_NAME):
        # this command creates the database
        with app.app_context():
            db.create_all()
        print("Created Database!")