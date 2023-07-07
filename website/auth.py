'''
    auth.py is going to have a roots related to authentication 
    like login, logout, sign up, etc.

    This file is a blueprint for the authentication views.
'''

from flask import Blueprint, render_template, redirect, url_for, views, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# this is the blueprint for the views
auth =  Blueprint('auth', __name__)


@auth.route('/sign-in', methods = ['GET', 'POST'])
def sign_in():
    # if the request is a POST request (meaning that the user is trying to sign in) then do this
    if request.method == 'POST':
        # this is how we get the data from these URLs or endpoints
        email = request.form.get("email")
        password = request.form.get("password")

        # if user with this email exists then do this
        user = User.query.filter_by(email=email).first()
        if user:
            # if the password is correct then do this
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                # this command logs the user in
                login_user(user, remember=True)
                # this command redirects the user to the home page
                return redirect(url_for('views.home'))
            # if the password is incorrect then do this
            else:
                flash("Incorrect password, try again.", category='error')

        # if user with this email does not exist then do this
        else:
            flash("Email does not exist.", category='error')
    
    return render_template("signin.html")

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    # if the request is a POST request (meaning that the user is trying to sign up) then do this
    if request.method == 'POST':
        # this is how we get the data from these URLs or endpoints
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
    
        # Check if user with this email is already in the database
        email_exists = User.query.filter_by(email=email).first()
        # Check if user with this username is already in the database
        username_exists = User.query.filter_by(username=username).first()

        # if the email already exists then do this
        if email_exists:
            flash("Email is already in use.", category='error')
        # if the username already exists then do this
        elif username_exists:
            flash("Username is already in use.", category='error')
        # if password1 and password2 are not the same then do this
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        # if length of username is less than 2 then do this
        elif len(username) < 2:
            flash("Username is too short.", category='error')
        # if length of password is less than 6 then do this
        elif len(password1) < 6:
            flash("Password is too short.", category='error')
        # if the email, username, and password are all valid then do this
        else:
            # add the user to the database. Here the password has been stored without being hashed which is a security issue
            # new_user = User(email=email, username=username, password=password1)
            # adding the user to the database with a hashed password
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            # command to add it to the database
            db.session.add(new_user)
            # write it to the database
            db.session.commit()
            # this command logs the user in
            login_user(new_user, remember=True)
            # flash a message that says that the account was created
            flash("Account created!", category='success')
            # redirect the user to the home page
            return redirect(url_for('views.home'))

    return render_template("signup.html")

@auth.route('/sign-out')
@login_required
def sign_out():
    # this command logs the user out
    logout_user()
    return redirect(url_for(views.home))