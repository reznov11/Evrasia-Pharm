from flask import Blueprint
profile_route = Blueprint('profile',__name__,static_folder='../static')
from . import views