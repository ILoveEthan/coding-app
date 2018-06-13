import datetime
import jwt

from flask import current_app
from project import db
from werkzeug.security import generate_password_hash

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(128), unique=True, nullable=False)
	email = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	active = db.Column(db.Boolean, default=True, nullable=False)
	admin = db.Column(db.Boolean, default=False, nullable=False) 

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password)


	def to_json(self):
		return {
			'id': self.id,
			'username': self.username,
			'email': self.email,
			'active': self.active,
			'admin': self.admin
		}

	def encode_auth_token(self, user_id):
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(
					days=current_app.config.get('TOKEN_EXPIRATION_DAYS'), 
					seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')),
				'iat': datetime.datetime.utcnow(),
				'sub': user_id
			}
			return jwt.encode(
				payload,
				current_app.config.get('SECRET_KEY'),
				algorithm='HS256'
			)
		except Exception as e:
			return e

	@staticmethod
	def decode_auth_token(auth_token):
		try:
			payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			return 'Signature expired. Please log in again.'
		except jwt.InvalidTokenError:
			return 'Invalid token. Please log in again.'