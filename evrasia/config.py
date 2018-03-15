# -*- coding: utf-8 -*-

import os
from flask import Markup
import datetime

# Get application current path
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Join the image directory with the application base direction
IMGDIR = os.path.abspath(os.path.join(BASEDIR, 'static/img'))

# Configuration object that contain the base configurations for the app
class Config(object):

	APP_NAME = 'Evrasia'

	# Generate secret key for application security
	SECRET_KEY = os.urandom(128).encode('base64')

	# Turn off sqlalchemy warnings
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Database username
	DB_USERNAME = ''

	# Database password
	DB_PASSWORD = ''

	# Database name
	DB_DATABASE = 'evrasia'
	
	# Database URI for connection
	SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@localhost:5432/%s'%(DB_USERNAME, DB_PASSWORD, DB_DATABASE)

	# Minifying all the html codes inside the templates
	MINIFY_PAGE = True

	# Types of data that the compressor will try to compress
	COMPRESS_MIMETYPES = ['text/css', 'text/xml', 'application/json', 'application/javascript']
	
	# The level of the compression
	COMPRESS_LEVEL = 6

	# Minimum size for the compressed file
	COMPRESS_MIN_SIZE = 500

	# Turn off ascii encoding from json requests, instead it will use by default UTF-8
	JSON_AS_ASCII = False

	# Not sorting the data inside a dictionary
	JSON_SORT_KEYS = False

	# My google api secret key
	RECAPTCHA_PUBLIC_KEY = ''
	RECAPTCHA_PRIVATE_KEY = ''

	# The name of the session that will appear inside browser
	SESSION_COOKIE_NAME = 'evrasia.pharm'

	# Type of saving session: [null, filesystem, redis, memcached, mongodb, sqlalchemy]
	SESSION_TYPE = 'filesystem'

	# The time that the session will still valid, here i set it to one week
	PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=7*24*60*60)

	# The table that the data inside session will get save into
	SESSION_SQLALCHEMY_TABLE = 'sessions'

	# The prefix key name for the session inside database
	SESSION_KEY_PREFIX = 'evrasia-pharm'

	# The direction where the session data will get saved
	SESSION_FILE_DIR = '/tmp/evrasia.pharm.Sessions'

	# Login token expiration
	REMEMBER_COOKIE_DURATION = datetime.timedelta(minutes=120)

	# Allow bootstrap files to serve locally not from the official site
	BOOTSTRAP_SERVE_LOCAL = True

	# Use the minified version of bootstrap
	BOOTSTRAP_USE_MINIFIED = True

	# This will insure that bootstrap using the last version
	BOOTSTRAP_QUERYSTRING_REVVING = True

	# Redirect if any error happens to index
	REDIRECT_BACK_DEFAULT = 'index'

	# The value for redirection inside cookies
	REDIRECT_BACK_COOKIE = 'back'

	# The direction where my images will gets uploaded
	UPLOADED_IMAGES_DEST = IMGDIR

	# The path to the folder
	UPLOADED_IMAGES_URL = '/static/images/'

	# Function to initiate the application context inside config file
	@staticmethod
	def init_app(app):
		pass

	META_TAGS = [Markup(
	'''
	<meta http-equiv="X-UA-Compatible" content="IE=7">
	<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
	<meta http-equiv="Expires" content="tue, 09 Jun 2019 19:45:00 GMT">
	<meta http-equiv="cache-control" content="public">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="keywords" content="Evrasia-Pharm magazine, Medicines internet magazine, Evrasia-Pharm Bishkek, Medical Pharmacy Evrasia, 
	Evrasia Pharm Kyrgyzstan, Evrasia Pharm KG, Designed By Evrasia Pharmacy, Pharmacy, Medical Pharmacy, Evrasia Pharm Online Magazine" />
	<meta name="author" content="Reznov - reznov110@gmail.com">
	<meta name="robots" content="index, follow">
	<meta name="revisit-after" content="3 month">
	<meta name="subject" content="Pharmacy internet magazine">
	<meta name="Description" content="Evrasia-Pharm internet magazine for selling medicines in Kyrgyzstan, Bishkek">
	<meta name="Geography" content="Kyrgyzstan, Bishkek">
	<meta name="Language" content="Russian">
	<meta name="Copyright" content="&copy;Evrasia-Pharm 2018">
	<meta name="Designer" content="Reznov">
	<meta name="Publisher" content="Evrasia-Pharm">
	<meta name="distribution" content="Global">
	<meta name="Robots" content="index,follow">
	<meta name="zipcode" content="7200001">
	<meta name="city" content="Bishkek">
	<meta name="country" content="Kyrgyzstan">
	<meta property="og:title" content="Evrasia-Pharm Internet Magazine" />
	<meta property="og:type" content="video.movie" />
	<meta property="og:url" content="http://www.evrasia-pharm.kg/" />
	<meta property="og:image" content="http://evrasia-pharm.kg/images/bground_image.jpg" />
	<meta property="og:description" content="Evrasia-Pharm internet magazine for selling medicines in Kyrgyzstan, Bishkek" />
	<meta property="og:determiner" content="Evrasia" />
	<meta property="og:locale" content="ru_RU" />
	<meta property="og:locale:alternate" content="en_US" />
	<meta property="og:site_name" content="Evrasia-Pharm" />
	'''
	)
	]

# This object is specified for production deployment only (Recommended when deploying the application)
class ProdConfig(Config):
	DEBUG = False

# This object is specified for development deployment only
class DevConfig(Config):

	DEBUG = True
	DEBUG_TB_INTERCEPT_REDIRECTS = False

	BROKER_URL = 'amqp://localhost//'
	CELERY_RESULT_BACKEND='amqp://localhost//'

	CELERY_ACCEPT_CONTENT = ['json','pickle']
	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_IGNORE_RESULT = False

	EVRASIA_EMAIL = 'evrasia-pharm.kg'
	# EVRASIA_MAIL_SUBJECT_PREFIX = 'Evrasia-Pharm.kg'
	EVRASIA_MAIL_SENDER = 'info@evrasia-pharm.kg'
	MAIL_SERVER = 'smtp.evrasia-pharm.kg'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USERNAME = ''
	MAIL_PASSWORD = ''
