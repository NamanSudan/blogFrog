'''
    views.py will have all the views related to the website
    like home page, profile page, etc.
'''

# Blueprint is a way to organize a group of related views and other code.
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# this is the blueprint for the views
views =  Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template("home.html", name=current_user.username)

