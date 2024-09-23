from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from ip_checker import check_ip_whitelist

db = SQLAlchemy()
login_manager = LoginManager()

