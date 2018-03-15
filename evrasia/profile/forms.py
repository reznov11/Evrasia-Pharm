#!-*- coding: utf-8 -*-

from flask_wtf import Form, RecaptchaField
from wtforms import validators, TextField, PasswordField, StringField, BooleanField, HiddenField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, InputRequired
from wtforms.fields.html5 import EmailField
from ..models import Subscriber, User
from ..helpers import validNumber
from validate_email import validate_email

class Subscribers(Form):
    email = EmailField(
        'Подпишитесь',
    	validators=[validators.DataRequired(message='Эл Почта нужна'), validators.Email(message='Неверный адрес электронной почты.'), validators.Length(max=100)]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Подпишись')

class Contact(Form):
    recaptcha = RecaptchaField()
    submit = SubmitField('Подпишись')

class Profile(Form):

    address = StringField('Адрес')

    telephone = StringField('Номер телефона')

    email = EmailField(
    	'Почта',
    	validators=[validators.Email(message='Неверный адрес электронной почты.'), validators.Length(max=100)]
    )

    password = PasswordField('Пароль')

    confirm_password = PasswordField('Подтвердите пароль')

    save = SubmitField('Сохранить изменения')

    # def validate(self):
    #     check_validate = super(Profile, self).validate()
    #     if not check_validate:
    #         return False
    #     if not validNumber(self.telephone.data):
    #         self.telephone.errors.append('Номер неправельный, пример: 996702123456')
    #         return False
    #     email_exist = User.query.filter_by(email=self.email.data).first()
    #     if email_exist:
    #         self.email.errors.append('E-mail уже регистрирован')
    #         return False
    #     if not validate_email(self.email.data):
    #         self.email.errors.append('E-mail неверный')
    #         return False
    #     if self.confirm_password.data != self.confirm_password.data:
    #         self.confirm_password.errors.append('Пароли должны совбодат')
    #         return False
    #     return True