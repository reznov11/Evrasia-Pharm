#-*- coding: utf-8 -*-

from flask import Flask, session, g
from jinja2 import Environment as EnvJinja
from .models import (
	db,
	User,
	Role,
	Category,
	Product,
	News
)
from .filters import *
from .extensions import *
from .admin_panel import *
from .admin_panel import CustomModelView, UserView, CategoryView, ProductsView, NewsView, CustomFileView
from .tasks import *
from datetime import datetime, timedelta

# Initiating all the libraries with my app
def create_app(config_object):
	app = Flask(__name__)
	app.config.from_object(config_object)
	app.url_map.strict_slashes = False
	session.modified = True

	######## Register Database ########

	db.init_app(app)
	csrf.init_app(app)

	######## Register Extentions ########

	login_manager.init_app(app)
	# toolbar.init_app(app)
	moment.init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)
	principal.init_app(app)
	htmlminify.init_app(app)
	jac.init_app(app)
	session.init_app(app)
	compress.init_app(app)
	mail.init_app(app)

	admin.init_app(app)

	admin.add_view(
		CustomModelView(
			Role, db.session
		)
	)
	admin.add_view(
		ProductsView(
			Product, db.session
		)
	)
	admin.add_view(
		UserView(
			User, db.session
		)
	)
	admin.add_view(
		CategoryView(
			Category, db.session
		)
	)
	admin.add_view(
		NewsView(
			News, db.session
		)
	)

	static_dir = os.path.join(os.path.dirname(__file__), 'static')
	admin.add_view(
		CustomFileView(
			static_dir,
			'/static/',
			name="Media"
		)
	)

	######## Register Application Routes ########
	
	from .main import main_route
	app.register_blueprint(main_route)

	from .catalog import catalog_route
	app.register_blueprint(catalog_route, url_prefix='/catalog')

	from .products import product_route
	app.register_blueprint(product_route, url_prefix='/products')

	from .profile import profile_route
	app.register_blueprint(profile_route, url_prefix='/profile')

	from .auth import auth_route
	app.register_blueprint(auth_route, url_prefix='/auth')

	return app