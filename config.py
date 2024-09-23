import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallbacksecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEOIP_DB = os.getenv('GEOIP_DB', 'app/static/GeoLite2-Country.mmdb')
    ALLOWED_COUNTRIES = 'all'


class DevelopmentConfig(Config):
    DATABASE_URL = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev.db')


class TestingConfig(Config):
    DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'sqlite:///test.db')


class ProductionConfig(Config):
    ALLOWED_COUNTRIES = os.getenv('PROD_ALLOWED_COUNTRIES', 'RU').split(',')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
