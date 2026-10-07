from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from Flask_Class.models import User
import os

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(
            username = username.data
        ).first()
        if user:
            raise ValidationError('This username is taken, please enter a different one')

    def validate_email(self, email):
            user = User.query.filter_by(
                email = email.data
            ).first()
            if user:
                raise ValidationError('This email is taken, please enter a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(
                username = username.data
            ).first()
            if user:
                raise ValidationError('This username is taken, please enter a different one')

    def validate_email(self, email):
            if email.data != current_user.email:
                user = User.query.filter_by(
                    email = email.data
                ).first()
                if user:
                    raise ValidationError('This email is taken, please enter a different one')

    def validate_picture(self, picture):
        if picture.data:
            picture.data.seek(0, os.SEEK_END)
            size = picture.data.tell()
            picture.data.seek(0)
        if size > 5 * 1024 * 1024:
            raise ValidationError('Image must be 5MB or smaller.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(
            email = email.data
        ).first()
        if user is None:
            raise ValidationError('There is no account with that email. If you do not receive an email, please check your spam folder or try again later.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Reset Password')