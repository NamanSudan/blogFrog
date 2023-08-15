'''
    auth.py is going to have routes related to authentication 
    like login, logout, sign up, etc.
'''

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, views
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from .models import User
from . import db, mail  # We import db and mail directly, as they are globally defined now.
from .email_service import send_email


# create an instance of URLSafeTimedSerializer for generating email confirmation tokens
def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

# this is the blueprint for the views
auth =  Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        # Extract the form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the user from the database (assuming you're using SQLAlchemy)
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct (you might need to handle password hashing)
        if user and check_password_hash(user.password, password):
            if user.email_confirmed:
                # You can now log the user in (using Flask-Login or similar extension)
                # For now, I'll use flash messages for demonstration
                flash('Logged in successfully!', 'success')
                return redirect(url_for('main.index')) # Redirect to main page after successful login
            else:
                flash('Please confirm your email address.', 'warning')
                return redirect(url_for('auth.unconfirmed'))
        
        flash('Invalid email or password!', 'danger')

    return render_template("signin.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        name = request.form.get('name')

        if not password1 or not password2:
            flash('Please fill out both password fields.')
            return redirect(url_for('auth.sign_up'))

        if password1 != password2:
            flash('Passwords do not match.')
            return redirect(url_for('auth.sign_up'))


        # # Check if user already exists by email or username
        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_email:
            flash('Email address already exists')
            return redirect(url_for('auth.sign_up'))
        
        if user_by_username:
            flash('Username already exists')
            return redirect(url_for('auth.sign_up'))
        
        # create a new user
        new_user = User(email=email, name=name, username=username, password=generate_password_hash(password1, method='sha256'), email_confirmed=False)
        db.session.add(new_user)
        db.session.commit()

        # generate a confirmation token and send a confirmation email
        token = get_serializer().dumps(email, salt='email-confirm')
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('email/confirm.html', confirm_url=confirm_url)
        # msg = Message('Please confirm your email', recipients=[email], html=html)
        # mail.send(msg)
        
        # Send the email using SendGrid
        send_email(email, 'Please confirm your email', html)


        return redirect(url_for('auth.unconfirmed'))

    return render_template("signup.html")


@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        # Try to extract email from the token
        email = get_serializer().loads(token, salt='email-confirm', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        flash('The confirmation link is invalid or expired.')
        return redirect(url_for('auth.unconfirmed'))
        
    # If the email was successfully extracted from the token
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Invalid confirmation link.')
        return redirect(url_for('auth.unconfirmed'))

    if user.email_confirmed:
        flash('Email already confirmed. Please log in.')
    else:
        user.email_confirmed = True
        db.session.commit()
        flash('Your email has been confirmed. Please log in.')

    return redirect(url_for('auth.sign_in'))

@auth.route('/unconfirmed')
def unconfirmed():
    return render_template('unconfirmed.html')

@auth.route('/sign-out')
def sign_out():
    return redirect(url_for(views.home))

@auth.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account associated with this email address.')
            return redirect(url_for('auth.reset_request'))

        token = get_serializer().dumps(user.email, salt='password-reset')
        reset_url = url_for('auth.reset_with_token', token=token, _external=True)
        html = render_template('email/reset.html', reset_url=reset_url)
        msg = Message('Reset your password', recipients=[user.email], html=html)
        mail.send(msg)

        flash('Password reset link has been sent to your email address.')
        return redirect(url_for('auth.sign_in'))

    return render_template('reset_request.html')

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = get_serializer().loads(token, salt='password-reset', max_age=86400)
    except:
        flash('The reset link is invalid or expired.')
        return redirect(url_for('auth.sign_in'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Invalid reset link.')
        return redirect(url_for('auth.sign_in'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        flash('Your password has been updated. Please log in.')
        return redirect(url_for('auth.sign_in'))

    return render_template('reset_with_token.html')

@auth.route('/resend-confirmation', methods=['GET', 'POST'])
def resend_confirmation():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account associated with this email address.')
            return redirect(url_for('auth.resend_confirmation'))
        if user.email_confirmed:
            flash('Email already confirmed. Please log in.')
            return redirect(url_for('auth.sign_in'))

        # If user exists and hasn't confirmed their email, send the email again
        token = get_serializer().dumps(email, salt='email-confirm')
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('email/confirm.html', confirm_url=confirm_url)
        send_email(email, 'Please confirm your email', html)
        
        flash('Confirmation email has been resent. Please check your inbox.')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('resend_confirmation.html')

@auth.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgot_password.html')

@auth.route('/forgot-password', methods=['POST'])
def forgot_password_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(email, salt='email-confirm')
        link = url_for('auth.reset_password', token=token, _external=True)
        
        msg = Message('Password Reset', sender='namansudans@gmail.com', recipients=[email])
        msg.body = f'Click on the link to reset your password: {link}'
        mail.send(msg)

        flash('A password reset link has been sent to your email.', 'info')
    
    return redirect(url_for('auth.sign_in'))

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.sign_in'))

    if request.method == 'POST':
        password = request.form.get('password')
        # Hash and update the user's password
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()

        flash('Your password has been reset!', 'success')
        return redirect(url_for('auth.sign_in'))

    return render_template('reset_password.html')
