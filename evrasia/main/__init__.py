from flask import Blueprint
main_route = Blueprint('main',__name__,static_folder='../static')
from . import views