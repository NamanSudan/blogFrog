# Description: This file is going to contain all the database models that we are going to use in our website
# this imports the database from the __init__.py file
from . import db 
# this imports the login manager from the __init__.py file
from flask_login import UserMixin
# this imports the login manager from the __init__.py file
from sqlalchemy.sql import func 

# define the first db model, which is going to be the user model
class User(db.Model, UserMixin):
    # Model is  just a table basically
    # UserMixin will allow us to use the login manager
    
    # this is the id of the user. primary_key means that it is unique
    id = db.Column(db.Integer, primary_key = True)
    # this is the email of the user. unique means that it is unique
    email = db.Column(db.String(150), unique = True)
    # this is the username of the user. unique means that it is unique
    username = db.Column(db.String(150), unique = True)
    # this is the password of the user
    password = db.Column(db.String(150))
    # this is the date that the user was created
    data_created = db.Column(db.DateTime(timezone=True), default=func.now())
    