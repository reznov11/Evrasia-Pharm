#!-*- coding: utf-8 -*-

import os, uuid
from ..models import *
from . import catalog_route
from ..extensions import csrf
from ..main.forms import Subscribers
from datetime import datetime
from flask import render_template, redirect, url_for, flash, session, current_app, request, g, send_from_directory, jsonify

@catalog_route.before_request
def categories():
	g.category = Category.query.order_by(Category.name)
	g.subscriber = Subscribers()
	items = session.get("cart", [])
	dict_of_products = {}
	for item in items:
		product = Product.query.filter_by(public_id=item).first()
		dict_of_products[product.public_id] = {"qty":1, "image": product.image, "title": product.title, "category":product.category.name, "price":product.price, 'slug':product.slug}
	g.shopping_cart = dict_of_products
	g.first_user_twitt = datetime.strptime('2018-01-12 13:14:44', '%Y-%m-%d %H:%M:%S')
	g.second_user_twitt = datetime.strptime('2018-01-29 17:36:12', '%Y-%m-%d %H:%M:%S')

@catalog_route.route('/')
def index():
	products = Product.query.order_by(Product.date.desc())
	return render_template('catalog/catalog.html', products=products)

@catalog_route.route('/<string:catalog_slug>')
def sluger(catalog_slug):
	get_category = Category.query.filter_by(slug=catalog_slug).first_or_404()
	products = Product.query.filter_by(category_id=get_category.id).order_by(Product.date.desc())
	title = get_category.name
	return render_template('catalog/catalog.html', title_catalog=title, products=products)

@catalog_route.route('/search', methods=['POST', 'GET'])
def search_product():
	if request.method == 'POST':
		get_query = request.form.get('productName', type=str)
		products = Product.query.filter(Product.title.ilike('%{}%'.format(get_query)))
		return render_template('catalog/search_results.html', results=products)
	return render_template('catalog/search_results.html')
