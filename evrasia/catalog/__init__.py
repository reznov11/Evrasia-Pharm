from flask import Blueprint
catalog_route = Blueprint('catalog',__name__,static_folder='../static')
from . import views