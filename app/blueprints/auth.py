from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли в аккаунт', 'success')
            return redirect(url_for('main.home'))  # Redirect to a protected route
        flash('Неверные данные', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Логин уже используется.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(username=form.username.data, password=form.password.data)  # Hash password here
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация завершена', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('main.welcome'))
