from flask import Blueprint
auth_route = Blueprint('auth',__name__,static_folder='../static')
from . import views