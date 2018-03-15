import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import request, redirect, url_for, Markup, current_app
from werkzeug import secure_filename

from flask_admin import Admin, form, AdminIndexView, BaseView, expose
from flask_admin import BaseView, expose
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from flask_login import current_user,login_required

from .extensions import admin_permission, base_slugify
from .models import db

from wtforms import FileField

file_path = os.path.join(os.path.dirname(__file__), 'static', 'images','thumbs')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class CustomModelView(ModelView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.is_admin
	# def inaccessible_callback(self, name, **kwargs):
	# 	return redirect(url_for('main.index', next=request.url))
	pass

class AdminIndex(AdminIndexView):
    @expose('/admin/')
    @login_required
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/matser.html')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('main.index', next=request.url))

class CustomFileView(FileAdmin):

	allowed_extensions = (
		'txt',
		'md',
		'js',
		'css',
		'html',
		'jpg',
		'gif',
		'png'
	)

	editable_extensions = ('md','html','js','css','txt')

	def is_accessible(self):
	    return current_user.is_authenticated and current_user.is_admin
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('main.index', next=request.url))

class CategoryView(CustomModelView):

	column_list = ('name','slug')
	form_excluded_columns = ('slug', 'products')

	def on_model_change(self, form, model, is_created):
		model.slug = base_slugify(model.name)
		db.session.commit()

class NewsView(CustomModelView):

	column_list = ('title','published', 'image')
	column_searchable_list = ('title', 'published')
	form_excluded_columns = ('slug')

	def on_model_change(self, form, model, is_created):

		image_path = os.path.join(current_app.root_path, 'static', 'images', 'products')

		# file = request.files['image']
		file = request.files.get(form.image.name)

		if file.filename == '':
			original_image = model.image
		
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			model.image = '/static/images/thumbs/' + filename
			file.save(os.path.join(image_path, filename))

		model.slug = base_slugify(model.title)
		db.session.commit()

	def _list_thumbnail(view, context, model, name):

		if not model.image:
			return ''

		if model.image:
			return Markup('<img src="{image}" style="width:100px;">'.format(image=model.image))

		return Markup('<img src="%s">' % url_for('static',
					filename='images/thumbs/'+form.thumbgen_filename(model.image)))

	form_overrides = {
		'image': form.FileUploadField
	}

	form_args = {
		'image': {
			'label': 'Product',
			'base_path': file_path,
			'allow_overwrite': False
		}
	}

	column_formatters = {
		'image': _list_thumbnail
	}

	form_extra_fields = {
		'image': form.ImageUploadField('Image',
		base_path=file_path,
		thumbnail_size=(100, 100, True))
	}

class ProductsView(CustomModelView):

	column_searchable_list = ('title', 'price')
	column_list = ('title','descr','price','image')
	column_filters = ('date', 'title', 'price')
	form_excluded_columns = ('public_id', 'products', 'rates', 'comments', 'slug', 'date')

	form_extra_fields = {
		"image": FileField('image')
	}

	def on_model_change(self, form, model, is_created):

		image_path = os.path.join(current_app.root_path, 'static', 'images', 'products')

		# file = request.files['image']
		file = request.files.get(form.image.name)

		if file.filename == '':
			original_image = model.image
		
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			model.image = '/static/images/thumbs/' + filename
			file.save(os.path.join(image_path, filename))

		model.slug = base_slugify(model.title)
		db.session.commit()

	def _list_thumbnail(view, context, model, name):

		if not model.image:
			return ''

		if model.image:
			return Markup('<img src="{image}" style="width:100px;">'.format(image=model.image))

		return Markup('<img src="%s">' % url_for('static',
					filename='images/thumbs/'+form.thumbgen_filename(model.image)))

	form_overrides = {
		'image': form.FileUploadField
	}

	form_args = {
		'image': {
			'label': 'Product',
			'base_path': file_path,
			'allow_overwrite': False
		}
	}

	column_formatters = {
		'image': _list_thumbnail
	}

	form_extra_fields = {
		'image': form.ImageUploadField('Image',
		base_path=file_path,
		thumbnail_size=(100, 100, True))
	}

class UserView(CustomModelView):
	column_list = ('username', 'roles', 'confirmed', 'is_admin', 'joined','image')

	column_searchable_list = ('username', 'id')
	column_filters = ('joined', 'email', 'username')

	path = os.path.abspath(
		os.path.join(
			os.path.dirname(__file__),
			os.pardir
		)
	)

	def on_model_change(self, form, model, is_created):
		path = os.path.abspath(
			os.path.join(
				os.path.dirname(__file__),
				os.pardir
			)
		)

		image_path = os.path.join(current_app.root_path, 'static', 'images')
		photo_data = request.files.get(form.image.name)

		if photo_data:
			name = secure_filename(photo_data.filename)
			model.image = '/static/images/thumbs/'+name
			photo_data.save(os.path.join(image_path, name))

	def _list_thumbnail(view, context, model, name):

		if model.image:
			return Markup('<img src="{avatar}" style="width:100px;">'.format(avatar=model.image))

		if not model.image:
			return Markup('<img src="{avatar}" style="width:100px;">'.format(avatar=model.avatar(100)))

		return Markup('<img src="%s" style="width:100px;">' % url_for('static',
					filename='images/thumbs/'+form.thumbgen_filename(model.image)))

	# Override form field to use Flask-Admin FileUploadField
	form_overrides = {
		'image': form.FileUploadField
	}

	# Pass additional parameters to 'image' to FileUploadField constructor
	form_args = {
		'image': {
			'label': 'User',
			'base_path': file_path,
			'allow_overwrite': False
		}
	}

	column_formatters = {
		'image': _list_thumbnail
	}

	# Alternative way to contribute field is to override it completely.
	# In this case, Flask-Admin won't attempt to merge various parameters for the field.
	form_extra_fields = {
		'image': form.ImageUploadField('User',
		base_path=file_path,
		thumbnail_size=(100, 100, True))
	}