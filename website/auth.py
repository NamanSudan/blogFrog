'''
    auth.py is going to have a roots related to authentication 
    like login, logout, sign up, etc.
'''

from flask import Blueprint, render_template, redirect, url_for, views

# this is the blueprint for the views
auth =  Blueprint('auth', __name__)

@auth.route('/sign-in')
def sign_in():
    return render_template("signin.html")

@auth.route('/sign-up')
def sign_up():
    return render_template("signup.html")

@auth.route('/sign-out')
def sign_out():
    return redirect(url_for(views.home))