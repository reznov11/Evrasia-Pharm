#!-*- coding: utf-8 -*-

import jinja2
import os, uuid
from ..models import *
from . import product_route
from ..extensions import csrf
from ..main.forms import Subscribers
from datetime import datetime
from ..helpers import parse_arg_from_requests
from flask import render_template, redirect, url_for, flash, session, current_app, request, g, send_from_directory, jsonify
from flask_login import current_user,login_required

@product_route.before_request
def categories():
    g.category = Category.query.order_by(Category.name)
    g.subscriber = Subscribers()
    items = session["cart"] if 'cart' in session else []
    dict_of_products = {}
    total_price = 0
    for item in items:
        product = Product.query.filter_by(public_id=item).first()
        total_price += product.price
        if product.public_id in dict_of_products:
            dict_of_products[product.public_id]["qty"] += 1
        else:
            dict_of_products[product.public_id] = {"qty":1, "image": product.image, "title": product.title, "category":product.category.name, "price":product.price, 'slug':product.slug}
    g.shopping_cart = dict_of_products
    g.total = total_price
    g.first_user_twitt = datetime.strptime('2018-01-12 13:14:44', '%Y-%m-%d %H:%M:%S')
    g.second_user_twitt = datetime.strptime('2018-01-29 17:36:12', '%Y-%m-%d %H:%M:%S')

@product_route.route('/<string:product_slug>')
def description(product_slug):
    product = Product.query.filter_by(slug=product_slug).first_or_404()
    comments = Comment.query.filter_by(product_id=product.id).order_by(Comment.date.desc())
    average = Rate.query.filter(Rate.product_id == product.id)
    return render_template('product/product.html', product=product, comments=comments, average=average)

@product_route.route("/cart", methods=['GET','POST'])
def shopping_cart():
    if "cart" not in session:
        return render_template("product/cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        dict_of_products = {}

        total_price = 0
        for item in items:
            product = Product.query.filter_by(public_id=item).first()
            total_price += product.price
            if product.public_id in dict_of_products:
                dict_of_products[product.public_id]["qty"] += 1
            else:
                dict_of_products[product.public_id] = {"qty":1, "image": product.image, "title": product.title, "category":product.category.name, "price":product.price, 'slug':product.slug}
        return render_template("product/cart.html", display_cart = dict_of_products, total = total_price)

@product_route.route("/add_to_cart/<string:product_id>", methods=['POST'])
def add_to_cart(product_id):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product_id)
    return jsonify({'cart':'Товар добавлен в корзину'})

@product_route.route("/delete-product/<string:product_id>", methods=['POST'])
def delete_product(product_id):
    if "cart" not in session:
        session["cart"] = []
    while product_id in session['cart']: session['cart'].remove(product_id)
    return jsonify({'cart':'Товар удален из корзины'})

@product_route.route("/delete-one-product/<string:product_id>", methods=['POST'])
def delete_one_product(product_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].remove(product_id)
    return jsonify({'cart':'Товар удален из корзины'})

@product_route.route("/clear-cart", methods=['POST'])
def clear_cart():
    if "cart" in session:
        if len(g.shopping_cart) > 0:
            session["cart"] = []
            return jsonify({'cart':'Корзина успешна очищена'})
    return jsonify({'cart':'Корзина пустая'})

@product_route.route('/add-comment', methods=['POST'])
def add_comment():
    if not current_user.is_authenticated:
        return redirect(url_for('catalog.index'))
    if request.method == 'POST':
        text = request.form['comment']
        product = request.form['productId']
        product = Product.query.filter_by(public_id=product).first()
        if product:
            comment = Comment()
            comment.text = jinja2.escape(text)
            comment.product_id = product.id
            comment.user_id = current_user.id
            db.session.add(comment)
            db.session.commit()
            return jsonify({'success':'Комментарии добавлно'})
        return jsonify({'error':'Error'}), 404
    return jsonify({'error':'Error'}), 405

@product_route.route('/rate', methods=['POST'])
def rate_product():
    if not current_user.is_authenticated:
        return redirect(url_for('catalog.index'))
    if request.method == 'POST':
        get_data = request.get_json()
        product_exist = Product.query.filter_by(public_id=str(get_data['productId'])).first()
        if product_exist.voted(current_user.id):
            return jsonify({'was_voted':'Уже поставили рейтинг'})
        if product_exist:
            vote = Rate()
            if int(get_data['rate_star']) == 1:
                vote.rate = 10
            if int(get_data['rate_star']) == 2:
                vote.rate = 20
            if int(get_data['rate_star']) == 3:
                vote.rate = 30
            if int(get_data['rate_star']) == 4:
                vote.rate = 40
            if int(get_data['rate_star']) == 5:
                vote.rate = 50
            if int(get_data['rate_star']) == 6:
                vote.rate = 60
            if int(get_data['rate_star']) == 7:
                vote.rate = 70
            if int(get_data['rate_star']) == 8:
                vote.rate = 80
            if int(get_data['rate_star']) == 9:
                vote.rate = 90
            if int(get_data['rate_star']) == 10:
                vote.rate = 100
            vote.user_id = current_user.id
            vote.product_id = product_exist.id
            db.session.add(vote)
            db.session.commit()

            average = Rate.query.filter(Rate.product_id == product_exist.id)
            return jsonify({
                'rating': product_exist.rating(average.count()),
                'count': product_exist.rates.count()
            })
        else:
            return jsonify({'notfound':'Продукт ненайдено'})
    return jsonify({'error':'Ошибка!'})

@product_route.route('/submit-order', methods=['GET'])
@login_required
def submit_order():
    return render_template('product/confirm_order.html')