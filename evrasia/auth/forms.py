#!-*- coding: utf-8 -*-

from flask import request
from flask_wtf import Form, RecaptchaField
from wtforms import validators, TextField, PasswordField, StringField, BooleanField, HiddenField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, InputRequired
from wtforms.fields.html5 import EmailField
from ..models import User
from ..helpers import validNumber

class LoginForm(Form):
    telephone = TextField(
        'Логин',
        validators=[validators.DataRequired(message='Это поле обязательно к заполнению.')]
    )
    password = PasswordField(
        'Пароль',
        validators=[validators.DataRequired(message='Это поле обязательно к заполнению.')]
    )
    # url_next = HiddenField('next')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(telephone=self.telephone.data).first()
        if not user:
            self.telephone.errors.append('Неверные учетные данные.')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Неверные учетные данные.')
            return False

        return True

class Registration(Form):

    fullname = StringField(
    	'ФИО',
    	validators=[validators.DataRequired(message='Имя нужно.'), validators.Length(max=20)]
    )

    email = EmailField(
    	'Почта',
    	validators=[validators.DataRequired(message='Эл Почта нужна'), validators.Email(message='Неверный адрес электронной почты.'), validators.Length(max=100)]
    )

    telephone = StringField('Номер телефона',
        [validators.Required(message='Номер телефона нужен.'), validators.Length(min=12, max=12, message='Номер телефон должен быт 12 цифра, например: 996702123456')]
    )

    password = PasswordField('Пароль', [
    	validators.Required(message='Пожалуйста введите пароль.'),
    	validators.Length(min=8, message='Пароль должен быт не меньше 8 символов.'),
    	validators.EqualTo('confirm_password', message="Пароли должны совпадать.")
    ])

    confirm_password = PasswordField('Подтвердите пароль')

    recaptcha = RecaptchaField('Recaptcha')

    register = SubmitField('Зарегистрироватся')

    def validate(self):
        check_validate = super(Registration, self).validate()
        if not check_validate:
            return False
        phone_exist = User.query.filter_by(telephone=self.telephone.data).first()
        if phone_exist:
            self.telephone.errors.append('Номер уже регистрирован')
            return False
        if not validNumber(self.telephone.data):
            self.telephone.errors.append('Номер неправельный, пример: 996702123456')
            return False
        email_exist = User.query.filter_by(email=self.email.data).first()
        if email_exist:
            self.email.errors.append('E-mail уже регистрирован')
            return False
        return True