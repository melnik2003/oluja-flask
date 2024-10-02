import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallbacksecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.db'
    GEOIP_DB = os.getenv('GEOIP_DB', 'app/static/GeoLite2-Country.mmdb')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_COUNTRIES = 'all'


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')
    ALLOWED_COUNTRIES = 'all'


class ProductionConfig(Config):
    ALLOWED_COUNTRIES = os.getenv('PROD_ALLOWED_COUNTRIES', 'RU').split(',')
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI', 'sqlite:///prod.db')
