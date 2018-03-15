#!-*- coding: utf-8 -*-

import os
from ..models import *
from . import profile_route
from .filters import *
from .forms import Subscribers, Profile
from ..tasks import send_email
from datetime import datetime
import jwt, base64
from flask import render_template, redirect, url_for, flash, session, current_app, request, g, jsonify
from flask_login import current_user, login_required
from validate_email import validate_email
from ..helpers import validNumber

@profile_route.before_request
def categories():
	g.category = Category.query.order_by(Category.name)
	g.subscriber = Subscribers()
	items = session["cart"] if 'cart' in session else []
	dict_of_products = {}
	for item in items:
		product = Product.query.filter_by(public_id=item).first()
		dict_of_products[product.public_id] = {"qty":1, "image": product.image, "title": product.title, "category":product.category.name, "price":product.price, 'slug':product.slug}
	g.shopping_cart = dict_of_products
	g.first_user_twitt = datetime.strptime('2018-01-12 13:14:44', '%Y-%m-%d %H:%M:%S')
	g.second_user_twitt = datetime.strptime('2018-01-29 17:36:12', '%Y-%m-%d %H:%M:%S')

@profile_route.route('/cabinet', methods=['GET','POST'])
@login_required
def cabinet():
	user = User.query.get(current_user.id)
	# cat_no_sub = Category.query.filter(Category.sub_menu == None)
	form = Profile(obj=user)
	if request.method == 'POST':
		form.populate_obj(user)
		original_password = user.password
		original_email = user.email
		original_telephone = user.telephone
		original_address = user.address
		if form.validate_on_submit():

			if form.address.data:
				user.address = form.address.data
			else:
				user.address = original_address

			if len(form.telephone.data) > 0:
				if not validNumber(form.telephone.data):
					flash('Номер неправельный, пример: 996702123456','danger')

				if form.telephone.data != original_telephone:
					phone_exist = User.query.filter_by(telephone=form.telephone.data).first()
					if phone_exist:
						flash('Номер уже регистрирован','danger')
					else:
						user.telephone = form.telephone.data

			if form.email.data is not None and form.email.data != original_email:
				if not validate_email(form.email.data):
					flash('E-mail неверный','danger')

				email_exist = User.query.filter_by(email=form.email.data).first()
				if email_exist:
					flash('E-mail уже регистрирован','danger')

				user.email = form.email.data

			if len(form.password.data) > 0:
				if not form.confirm_password.data == form.password.data:
					flash('Пароли должны совпадать','danger')
				else:
					user.set_password(form.password.data)
			else:
				user.password = original_password
			db.session.commit()
			return redirect(url_for('profile.cabinet'))
		return redirect(url_for('profile.cabinet'))
	return render_template('profile/index.html', form=form, action='visit')

# @profile_route.route('/orders-history', methods=['POST'])
# @login_required
# def orders_history():
# 	return render_template('profile/index.html', form=form, action='edit')