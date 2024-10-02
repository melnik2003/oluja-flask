from flask import current_app, Blueprint, render_template, send_from_directory

from app import ip_handler

main_bp = Blueprint('main', __name__)


@main_bp.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


@main_bp.route('/')
def welcome():
    ip_handler.check_ip()
    return render_template('welcome.html')
