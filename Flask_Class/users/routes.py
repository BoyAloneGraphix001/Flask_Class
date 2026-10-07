from flask import Blueprint, current_app, render_template, url_for, flash, redirect, request
from Flask_Class import db
from Flask_Class.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from Flask_Class.models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from Flask_Class.users.utils import save_picture, delete_picture, send_reset_email
import os

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    title = "Register Page"
    if form.validate_on_submit():
        existing_user = db.session.execute(db.select(User).where (User.email == form.email.data)).scalar_one_or_none()
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_password
            )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log-in', 'success')  
        return redirect(url_for('users.login'))
    return render_template('register.html', title=title, form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    title = "Login Page"
    if form.validate_on_submit():
        user = User.query.filter_by(
            email = form.email.data
        ).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title=title, form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    title = 'Account Page'
    if form.validate_on_submit():
        if form.picture.data:
            old_picture = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            delete_picture(old_picture)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    picture_path = os.path.join(current_app.root_path, 'static/images', current_user.image_file)
    filename = current_user.image_file if os.path.exists(picture_path) else 'default.jpeg'
    image_file = url_for('static', filename='images/' + filename)
    return render_template('account.html', title = title, image_file = image_file, form = form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log-in', 'success')  
            return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)