#!-*- coding: utf-8 -*-

import os, uuid
from ..models import *
from . import main_route
from ..extensions import csrf
from .filters import *
from .forms import Subscribers, Contact
from flask_login import current_user
from ..tasks import send_email
import jwt, base64
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import render_template, redirect, url_for, flash, session, current_app, request, g, send_from_directory, jsonify

@main_route.before_request
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

@main_route.route('/icons/<string:filename>')
def images(filename):
	return send_from_directory(os.path.join(current_app.root_path, 'static', 'images', 'icons'), filename)

@main_route.route('/css_provider/<string:filename>')
def css_provider(filename):
	return send_from_directory(os.path.join(current_app.root_path, 'static', 'css'), filename)

@main_route.route('/js_provider/<string:filename>')
def js_provider(filename):
	return send_from_directory(os.path.join(current_app.root_path, 'static', 'js'), filename)

@main_route.route('/')
@main_route.route('/pharm')
def index():
	products = Product.query.order_by(Product.date.desc()).limit(4)
	return render_template('home/home.html', products=products)

@main_route.route('/about')
def about():
	return render_template('home/about.html')

@main_route.route('/our-team')
def team():
	return render_template('home/team.html')

@main_route.route('/vacancies')
def vacancy():
	return render_template('home/job.html')

@main_route.route('/cooperation')
def cooperation():
	return render_template('home/cooperation.html')

@main_route.route('/for-corporate-clients-and-legal-entities/')
def corporate():
	return render_template('home/corporate.html')

@main_route.route('/news')
def news():
	latest_news = News.query.order_by(News.published.desc())
	return render_template('home/news.html', news=latest_news)

@main_route.route('/bacteriophages')
def bacterio():
	return render_template('home/bacterio.html')

@main_route.route('/how-to-order')
def hw_order():
	return render_template('home/how-to-order.html')

@main_route.route('/delivery-and-shipping')
def delivery():
	return render_template('home/delivery.html')

@main_route.route('/certificates-and-licenses')
def certificates_and_licenses():
	return render_template('home/certificates.html')

@main_route.route('/contact', methods=['GET','POST'])
def contact():
	form = Contact()
	if request.method == 'POST':
		if form.validate_on_submit():
			letter = Letters()
			letter.fullname = form.fullname.data
			letter.telephone = form.telephone.data
			letter.email = form.email.data
			letter.subject = form.subject.data
			letter.message = form.message.data
			if current_user.is_authenticated:
				letter.user_id = current_user.id
			db.session.add(letter)
			db.session.commit()
			date_now = datetime.now()
			send_email(current_app.config['EVRASIA_MAIL_SENDER'], 'Новое письмо от {}'.format(form.fullname.data),'home/newsletter/new_letter', email=form.email.data, fullname=form.fullname.data, telephone=form.telephone.data, title=form.subject.data, message=form.message.data, sent=date_now)
			flash('Ваше сообщение успешно отправлено, мы вам отвечаем, но как можно скорее', 'success')
			return redirect(url_for('main.index'))
	return render_template('home/contact.html', form=form)

# @main_route.route('/checkout', methods=['POST'])
# def checkout():
# 	fake_dict = []
# 	for key, value in request.form.iteritems():
# 		if key.startswith('item_name'):
# 			print key
# 			print value
# 		if key.startswith('quantity'):
# 			print value
# 			fake_dict.append(value)
# 	# print len(fake_dict)
# 	return 'Checkout page'

@main_route.route('/subscribe', methods=['POST'])
def subscribe():
	form = g.subscriber
	if request.method == 'POST':
		if g.subscriber.validate_on_submit():
			email_exist = Subscriber.query.filter_by(email=form.email.data).first()
			if email_exist:
				flash('Вы уже являетесь подписчиком', 'info')
				return redirect(url_for('main.index'))
			subscribe = Subscriber(email=form.email.data)
			db.session.add(subscribe)
			db.session.commit()
			date_now = datetime.now()
			token = subscribe.generate_confirmation_token()
			send_email(form.email.data, 'Подтвердите подписку на рассылку','home/newsletter/confirm_subscribtion', token=token, email=form.email.data, sent=date_now)
			flash('Письмо было отпрвлено на ваш email {email}'.format(email=form.email.data), 'success')
			return redirect(url_for('main.index'))
	return redirect(url_for('main.index')+"#subscribe")

@main_route.route('/confirm/<token>')
def confirm_subscription(token):
	parse_token = str(token.split('.')[1])
	fetch_email = base64.urlsafe_b64decode(parse_token+'===')
	get_email = eval(fetch_email)['confirm']
	get_subscriber = Subscriber.query.filter_by(email=get_email).first()
	if get_subscriber is None:
		return redirect(url_for('main.index'))
	if get_subscriber.confirmed:
		flash('Вы уже являетесь подписчиком', 'info')
		return redirect(url_for('main.index'))
	if get_subscriber.confirm(token):
		get_subscriber.confirmed = True
		db.session.commit()
		flash('Вы успешна подтвердили подписку, спасибо.', 'success')
	else:
		flash('Ссылка для подтверждения является недействительным или истек.', 'danger')
	return redirect(url_for('main.index'))

@main_route.route('/unsubscribe/<string:token>')
def unsubscribe(token):
	parse_token = str(token.split('.')[1])
	fetch_email = base64.urlsafe_b64decode(parse_token+'===')
	get_email = eval(fetch_email)['confirm']
	get_subscriber = Subscriber.query.filter_by(email=get_email).first()
	if get_subscriber is None:
		return redirect(url_for('main.index'))
	if get_subscriber.confirm(token):
		db.session.delete(get_subscriber)
		db.session.commit()
		flash('Ваша подписка отменена.', 'success')
		return redirect(url_for('main.index'))
	return redirect(url_for('main.index'))
