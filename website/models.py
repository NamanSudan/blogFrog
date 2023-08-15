from .database import db
#from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    # Model is  just a table basically
    # UserMixin will allow us to use the login manager
    
    # this is the id of the user. primary_key means that it is unique
    id = db.Column(db.Integer, primary_key = True)
    # this is the name of the user
    name = db.Column(db.String(150))
    # this is the email of the user. unique means that it is unique
    email = db.Column(db.String(150), unique = True)
    # this is the username of the user. unique means that it is unique
    username = db.Column(db.String(150), unique = True)
    # this is the password of the user
    password = db.Column(db.String(150))
    # this is the date that the user was created
    data_created = db.Column(db.DateTime(timezone=True), default=func.now())
    email_confirmed = db.Column(db.Boolean, default=False)

