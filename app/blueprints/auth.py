from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/welcome')
def login():
    return render_template('auth/welcome.html')


@auth_bp.route('/logout')
def logout():
    # Add logout logic here
    return redirect(url_for('main.index'))