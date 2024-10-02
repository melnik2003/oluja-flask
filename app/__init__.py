from flask import Flask
from dotenv import load_dotenv
import os

from app.extensions import ip_handler
from app.extensions import db
from app.extensions import migrate
from app.extensions import socketio

from app.models import db_models

from app.blueprints import blueprints


def load_config(app):
    load_dotenv()
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif env == 'testing':
        app.config.from_object('config.TestingConfig')
    elif env == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')


# Factory function to create the Flask app
def create_app():
    app = Flask(__name__)

    load_config(app)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    ip_handler.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
