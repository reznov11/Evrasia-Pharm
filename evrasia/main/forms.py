#!-*- coding: utf-8 -*-

from flask_wtf import Form, RecaptchaField
from wtforms import validators, TextField, PasswordField, StringField, BooleanField, HiddenField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, InputRequired
from wtforms.fields.html5 import EmailField
from ..models import Subscriber

class Subscribers(Form):
    email = EmailField(
        'Подпишитесь',
    	validators=[validators.DataRequired(message='Эл Почта нужна'), validators.Email(message='Неверный адрес электронной почты.'), validators.Length(max=100)]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Подпишись')

class Contact(Form):
    fullname = StringField(
    	'ФИО',
    	validators=[validators.DataRequired(message='поля нужна.'), validators.Length(max=20)]
    )
    email = EmailField(
    	'Почта',
    	validators=[validators.DataRequired(message='Почта нужна'), validators.Email(message='Неверный адрес электронной почты.'), validators.Length(max=100)]
    )

    telephone = StringField('Номер телефона',
        [validators.Required(message='Номер телефона нужен.'), validators.Length(min=7, max=14, message='номер телефона должен быть от 7 до 14 цифров, например: 996702123456')]
    )
    subject = StringField(
    	'Тема',
    	validators=[validators.DataRequired(message='тема нужна.'), validators.Length(min=12, max=50, message='Ваше сообщение не должно быт меньшее 12 и больше 50 симолов по длину')]
    )
    message = TextAreaField(
        'Напишите что нибуд ...',
        validators=[validators.DataRequired(message='Напишите ваше сообщение!')]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Подпишись')