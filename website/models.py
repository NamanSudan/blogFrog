# Description: This file is going to contain all the database models that we are going to use in our website
# this imports the database from the __init__.py file
from . import db 
# this imports the login manager from the __init__.py file
from flask_login import UserMixin
# this imports the login manager from the __init__.py file
from sqlalchemy.sql import func 

# Define the blog post model
class Post(db.Model):
    # this is the id of the post
    id = db.Column(db.Integer, primary_key=True)
    # this is the title of the post
    title = db.Column(db.String(100))
    # this is the content of the post
    content = db.Column(db.Text)
    # this is the date of the post
    date = db.Column(db.DateTime(timezone=True), default=func.now())

