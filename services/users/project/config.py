import os

class BaseConfig(object):
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY')
	TOKEN_EXPIRATION_DAYS = 30
	TOKEN_EXPIRATION_SECONDS = 0

class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(BaseConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
	TOKEN_EXPIRATION_DAYS = 0
	TOKEN_EXPIRATION_SECONDS = 5

class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')