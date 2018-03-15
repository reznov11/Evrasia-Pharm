from flask import Blueprint
product_route = Blueprint('products',__name__,static_folder='../static')
from . import views