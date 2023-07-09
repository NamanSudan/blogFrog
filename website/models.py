from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

