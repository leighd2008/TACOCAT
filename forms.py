from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class TacoForm(FlaskForm):
    protein = TextAreaField("What kind of protein do you want on your Taco?", validators=[DataRequired()])
    shell = TextAreaField("What kind of shell do you want to use for your Taco?", validators=[DataRequired()])
    cheese = TextAreaField("Would you like cheese on your Taco?", validators=[DataRequired()])
    extras = TextAreaField("Please tell me any extras you would like on your Taco!", validators=[DataRequired()])
