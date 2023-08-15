from flask import Flask
from os import path
from flask_login import LoginManager
import psycopg2
import os
from dotenv import load_dotenv

from .database import db, init_app  # Import the already initialized `db` object from `database.py`
from flask_mail import Mail

from flask_migrate import Migrate
from .models import Post  # Assuming User and Post are your models

from flask_apscheduler import APScheduler
import datetime
from .models import User  # assuming your models are in a file called models.py in the same package/directory

from .main import main  # Import the main blueprint

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Initialize mail and db outside the create_app function.
mail = Mail()

def cleanup_unconfirmed_users():
    THRESHOLD_TIME = 86400  # 24 hours in seconds
    # query users who have not confirmed their email in the last 24 hours
    # assuming you have a datetime field named `created_at` in your User model
    unconfirmed_users = User.query.filter(User.created_at < datetime.datetime.utcnow() - datetime.timedelta(seconds=THRESHOLD_TIME), User.email_confirmed==False).all()
    for user in unconfirmed_users:
        db.session.delete(user)
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  
    
    # Initialize the scheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # Add the cleanup job, which will run every 24 hours
    scheduler.add_job(id='cleanup', func=cleanup_unconfirmed_users, trigger='interval', hours=24)

    # Set up migration
    migrate = Migrate(app, db)

    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('SMTP_HOST')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    mail.init_app(app)
    
    init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')  # Register the main blueprint

    return app
