#-*- coding: utf-8 -*-

from .models import User
from celery import Celery
from flask_mail import Mail
from flask_admin import Admin
from flask_moment import Moment
from flask_htmlmin import HTMLMIN
from flask_session import Session
from jac.contrib.flask import JAC
from flask_compress import Compress
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from jinja2 import Environment as EnvJinja
from celery.backends.redis import RedisBackend
from slugify import slugify, Slugify, UniqueSlugify
from flask_debugtoolbar import DebugToolbarExtension
from flask_principal import Principal, Permission, RoleNeed

# Static Admin for flask application
admin = Admin(name='Evrasia-Pharm', template_mode='bootstrap3')

# For creating jinja filters inside template (For interaction between Front-end and Back-end)
environment = EnvJinja()

# For allowing compression inside template
jac = JAC()

# These are the main configurations for application login system 
login_manager = LoginManager()

# URL to redirect if login needed
login_manager.login_view = 'auth.login'

# The strength of session protection
login_manager.session_protection = "strong"

# A message that will appear if the user entered a not authorized page
login_manager.login_message = u"Пожалуйста, войдите, чтобы получить доступ к этой странице."

# The main category for styling the alert inside template, [success, warning, danger, info] 
login_manager.login_message_category = "warning"

# If the user left the site for a period of time then this message will appear asking him to re-login
login_manager.needs_refresh_message = 'Вам необходимо повторно войти на сайт, чтобы получить доступ к этой странице'

# A tool for monitoring and debugging application from the browser
toolbar = DebugToolbarExtension()

# Library that takes care of the appearance of time inside template
moment = Moment()

# Bootstrap package for simplifying the creation of the Front-end
bootstrap = Bootstrap()

# Sluger to prettify the texts inside url
base_slugify = Slugify(to_lower=True)

# Minifying HTML codes
htmlminify = HTMLMIN()

# Cross site request forgery protection to prevent any request coming to the site from others
csrf = CSRFProtect()

# The session manager
session = Session()

# Compressor for all types of data [xml, zip, js, css]
compress = Compress()

# Principal for organizing the authorization and the user information inside the app
principal = Principal()

# Two main roles for my users
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

# Sending emails to the cloud
mail = Mail()

# Run tasks with celery
celery = Celery()
celery.backend = RedisBackend(app=celery)

# Function to load the logged user id into flask_login then to save it as an "current_user" object
@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)