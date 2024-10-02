from flask import Flask
from dotenv import load_dotenv
import os

from app.extensions import IPHandler
from app.extensions import db
from app.extensions import migrate
from app.extensions import socketio

from app.models import db_models

from app.blueprints import blueprints


# Custom Flask app class with additional functionality
class CustomFlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ip_handler = None

    def init_ip_handler(self):
        self.ip_handler = IPHandler(self.config.get('GEOIP_DB'),
                                    self.config.get('ALLOWED_COUNTRIES'))

    # Function to load configuration based on environment
    def load_config(self):
        load_dotenv()
        match os.getenv('FLASK_ENV'):
            case 'development':
                self.config.from_object('config.DevelopmentConfig')
            case 'testing':
                self.config.from_object('config.TestingConfig')
            case 'production':
                self.config.from_object('config.ProductionConfig')
            case _:
                self.config.from_object('config.DevelopmentConfig')


# Factory function to create the Flask app
def create_app():
    app = CustomFlaskApp(__name__)

    app.load_config()

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    app.init_ip_handler()

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
