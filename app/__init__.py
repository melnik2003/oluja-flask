from flask import Flask
import os

from app.extensions import check_ip_whitelist, db, login_manager
from blueprints import blueprints


def create_app():
    app = Flask(__name__)

    match os.getenv('FLASK_ENV').lower():
        case 'development':
            app.config.from_object('config.DevelopmentConfig')
        case 'testing':
            app.config.from_object('config.TestingConfig')
        case 'production':
            app.config.from_object('config.ProductionConfig')
        case _:
            app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    check_ip_whitelist(app.config.GEOIP_DB, app.config.ALLOWED_COUNTRIES)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'welcome'

    # Register the blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
