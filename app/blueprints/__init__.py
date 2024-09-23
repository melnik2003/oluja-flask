from flask import Blueprint
from . import main, auth

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

blueprints = (main_bp, auth_bp)