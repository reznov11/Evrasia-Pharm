# -*- coding: utf-8 -*-

from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import uuid

db = SQLAlchemy()

# Many-to-Many table that contain each user role
roles = db.Table(
	'role_users',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
	db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
)

class Role(db.Model):

	__tablename__ = 'role'

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(), unique=True)
	description = db.Column(db.String())

	def __repr__(self):
		return '{}'.format(self.name)

class User(db.Model):

	__tablename__ = 'user'

	id = db.Column(db.Integer(), primary_key=True)
	public_id = db.Column(db.String(36))
	username = db.Column(db.String(255))
	slug = db.Column(db.String(255))
	password = db.Column(db.String(93))
	email = db.Column(db.String(80))
	address = db.Column(db.String(100))
	telephone = db.Column(db.String(12))
	is_admin = db.Column(db.Boolean(), default=False)
	joined = db.Column(db.DateTime(), default=datetime.utcnow)
	confirmed = db.Column(db.Boolean(), default=False)
	image = db.Column(db.String(255))

	comments = db.relationship('Comment', backref='user', lazy='dynamic')

	letters = db.relationship('Letters', backref='user', lazy='dynamic')

	roles = db.relationship(
		'Role',
		secondary=roles,
		backref=db.backref('users', lazy='joined',
		passive_deletes=True,
		single_parent=True)
	)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	def __repr__(self):
		return '{}'.format(self.username)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, value):
		return check_password_hash(self.password, value)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def get_token(self, expiration=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'user': self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		id = data.get('user')
		if id:
			return User.query.get(id)
		return None

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(255), default=uuid.uuid4)
	title = db.Column(db.String(255))
	slug = db.Column(db.String(255), unique=True)
	descr = db.Column(db.Text())
	price = db.Column(db.Float())
	image = db.Column(db.String(255))
	date = db.Column(db.DateTime(), default=datetime.utcnow)

	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	# categories = db.relationship('Category', backref='product', lazy='dynamic')
	rates = db.relationship('Rate', backref='product', lazy='dynamic')
	comments = db.relationship('Comment', backref='product', lazy='dynamic')

	def rating(self, all_rates):
		rates = db.session.query(
		    db.func.sum(Rate.rate)
		).filter(Rate.product_id == self.id)

		if rates[0] != (None):
			return "{:.1f}".format(sum(rates[0]) / float(all_rates) * 10 / 100)
		else:
			return 0

	def voted(self, user):
		get_vote  = Rate.query.filter_by(user_id=user, product_id=self.id).first()
		if get_vote:
			return True
		return False

	def __repr__(self):
		return "{title}".format(title=self.title[0:20])

class Rate(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	rate = db.Column(db.Integer())
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	product_id = db.Column(db.Integer(), db.ForeignKey('product.id'))

	def __repr__(self):
		return "{}".format(self.rate)

class Comment(db.Model):

	id = db.Column(db.Integer(), primary_key=True)
	text = db.Column(db.Text())
	live = db.Column(db.Boolean(), default=True)
	date = db.Column(db.DateTime(), default=datetime.utcnow)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	product_id = db.Column(db.Integer(), db.ForeignKey('product.id'))

	def __repr__(self):
		return 'Comment: {}'.format(self.text[:15])

class Subscriber(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	email = db.Column(db.String(100), unique=True)
	confirmed = db.Column(db.Boolean(), default=False)
	date = db.Column(db.DateTime(), default=datetime.utcnow)

	def generate_confirmation_token(self, expiration=5184000): #datetime.now() + timedelta(days=1, hours=23, minutes=59, seconds=59, microseconds=999999)
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.email})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.email:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	@staticmethod
	def verify_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		id = data.get('user')
		if id:
			return User.query.filter_by(email=id)
		return None

	def __repr__(self):
		return "{email}".format(email=self.email)

class News(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	slug = db.Column(db.String(255), unique=True)
	body = db.Column(db.Text())
	image = db.Column(db.String(255))
	published = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return "{title}".format(title=self.title)

class Category(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	slug = db.Column(db.String(100))

	products = db.relationship('Product', backref='category', lazy='dynamic')

	def __repr__(self):
		return "Category: {name}".format(name=self.name)

class Letters(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(100))
	email = db.Column(db.String(100))
	telephone = db.Column(db.String(14))
	subject = db.Column(db.String(50))
	message = db.Column(db.Text())
	sent = db.Column(db.DateTime(), default=datetime.utcnow)

	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), default=None)

	def __repr__(self):
		return "Subject: {sub}".format(sub=self.subject)