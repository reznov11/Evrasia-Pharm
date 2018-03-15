#!-*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, session, g, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import (
	Identity,
	AnonymousIdentity,
	identity_changed
)
from ..models import User, db, Role, Category, Product
from . import auth_route
from datetime import datetime, timedelta
from validate_email import validate_email
from .forms import LoginForm, Registration
from ..tasks import send_email
from ..extensions import base_slugify
from ..main.forms import Subscribers

@auth_route.before_request
def auth_forms():
	g.login = LoginForm()
	g.register = Registration()
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

@auth_route.route('/login', methods=['GET','POST'])
def login(title="Sign up & Login"):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	if request.method == 'POST':
		if g.login.validate_on_submit():

			get_user = User.query.filter_by(telephone=g.login.telephone.data).first()

			if get_user:
				if get_user.check_password(g.login.password.data):

					if g.login.remember_me.data:
						login_user(get_user, remember=True)

					login_user(get_user, remember=False)

					identity_changed.send(
						current_app._get_current_object(),
						identity=Identity(get_user.id)
					)
					next_ = request.form.get('next')
					if next_ != 'None':
						return redirect(next_)
					else:
						return redirect(url_for('main.index'))
				else:
					flash('Логин или пароль неверные.', "danger")
					return redirect(request.url)
				return redirect(url_for('auth.login'))
	return render_template('home/authorizations.html', title=title)

@auth_route.route('/registration', methods=['GET', 'POST'])
def registration():

	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	if g.register.validate_on_submit():

		user = User()
		user.fullname = g.register.fullname.data
		user.email = g.register.email.data
		user.telephone = g.register.telephone.data
		user.set_password(g.register.password.data)
		user.image = user.avatar(100)
		user.is_admin = False
		user_role = Role.query.filter_by(name="user").first()
		user.roles.append(user_role)
		user.username = g.register.fullname.data
		user.slug = base_slugify(g.register.fullname.data)
		db.session.add(user)
		db.session.commit()

		date_now = datetime.now()
		
		token = user.generate_confirmation_token()

		send_email(user.email, 'Подтвердите учетной записи','home/newsletter/confirm_account', token=token, username=user.fullname, sent=date_now)

		flash('Зайдите в ваш почтовый ящик {email}, перейдите по ссылке в письме'.format(email=user.email), 'info')
		return redirect(url_for('main.index'))
	return render_template('home/registration.html')

@auth_route.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.is_authenticated and current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		email = User.query.filter_by(email=current_user.email).first()
		email.confirmed = True
		db.session.add(email)
		db.session.commit()
		flash('Вы подтвердили свой email, спасибо.', 'success')
	else:
		flash('Ссылка для подтверждения является недействительным или истек.', 'danger')
	return redirect(url_for('main.index'))

@auth_route.route('/re-confirm')
@login_required
def resend_confirmation():
	if current_user.is_authenticated and current_user.confirmed:
		return redirect(url_for('main.index'))
	token = current_user.generate_confirmation_token()
	date_now = datetime.now()
	send_email(current_user.email, 'Подтвердите учетной записи','home/newsletter/confirm_account', token=token, username=current_user.fullname, sent=date_now)
	flash('Новое подтверждение по электронной почте отправлен вам по электронной почте {email}.'.format(email=current_user.email), 'info')
	return redirect(url_for('main.index'))

@auth_route.route('/logout')
def logout():
	logout_user()

	identity_changed.send(
		current_app._get_current_object(),
		identity=AnonymousIdentity()
	)
	return redirect(url_for('main.index'))