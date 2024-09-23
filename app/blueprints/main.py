from flask import render_template, send_from_directory
from . import main_bp


@main_bp.route("/robots.txt")
def robots():
    return send_from_directory('static', 'robots.txt')


@main_bp.route('/')
def index():
    return render_template('main/index.html')


