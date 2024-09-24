from flask import render_template, send_from_directory
from flask_login import login_required

from . import main_bp


@main_bp.route("/robots.txt")
def robots():
    return send_from_directory('static', 'robots.txt')


@main_bp.route('/')
@login_required
def home():
    return render_template('home.html')


@main_bp.route('/welcome')
def welcome():
    return render_template('welcome.html')