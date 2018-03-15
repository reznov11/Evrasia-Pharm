from flask import Markup, session
from .extensions import environment
from main import main_route

@main_route.app_template_filter('save_token')
def save_token(token):
	session['csrf_session_token'] = token
	return Markup("<input type='hidden' value='{token_session}'".format(token_session=token))
environment.filters['save_token'] = save_token