from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from sqlalchemy import or_, exc

from project.api.models import User
from project import db

bp = Blueprint('auth', __name__)

def add_user(username, email, password):
	user = User(
		username=username,
		email=email,
		password=password
	)
	db.session.add(user)
	db.session.commit()
	return user


@bp.route('/auth/register', methods=['POST'])
def register_user():
	post_data = request.get_json()
	response_object = {
		'status': 'fail',
		'message': 'Invalid payload.'
	}
	if not post_data:
		return jsonify(response_object), 400
	username = post_data.get('username')
	email = post_data.get('email')
	password = post_data.get('password')
	try:
		user = User.query.filter(or_(User.username==username, User.email==email)).first()
		if not user:
			new_user = add_user(username, email, password)
			auth_token = new_user.encode_auth_token(new_user.id)
			response_object = {
				'status': 'success',
				'message': 'Successfully registered.',
				'auth_token': auth_token.decode(),
			}
			return jsonify(response_object), 201
		else:
			response_object['message'] = 'Sorry. That user already exists.'
			return jsonify(response_object), 400
	except (exc.IntegrityError, TypeError) as e:
		db.session.rollback()
		return jsonify(response_object), 400


@bp.route('/auth/login', methods=['POST'])
def login_user():
	post_data = request.get_json()
	response_object = {
		'status': 'fail',
		'message': 'Invalid payload.'
	}
	if not post_data:
		return jsonify(response_object), 400
	email = post_data.get('email')
	password = post_data.get('password')
	try:
		user = User.query.filter_by(email=email).first()
		if user and check_password_hash(user.password, password):
			auth_token = user.encode_auth_token(user.id)
			response_object = {
				'status': 'success',
				'message': 'Successfully logged in.',
				'auth_token': auth_token.decode()
			}
			return jsonify(response_object), 200
		elif not user:
			response_object['message'] = 'User does not exist.'
			return jsonify(response_object), 404
		else:
			response_object['message'] = 'Wrong password.'
			return jsonify(response_object), 404
	except Exception as e:
		response_object['message'] = 'Try again.'
		return jsonify(response_object), 500


@bp.route('/auth/logout', methods=['GET'])
def logout_user():
	auth_header = request.headers.get('Authorization')
	response_object = {
		'status': 'fail',
		'message': 'Provide a valid auth token.'
	}
	if auth_header:
		auth_token = auth_header.split(' ')[1]
		resp = User.decode_auth_token(auth_token)
		if not isinstance(resp, str):
			response_object = {
				'status': 'success',
				'message': 'Successfully logged out.'
			}
			return jsonify(response_object), 200
		else:
			response_object['message'] = resp
			return jsonify(response_object), 401
	else:
		return jsonify(response_object), 403


@bp.route('/auth/status', methods=['GET'])
def status():
	auth_header = request.headers.get('Authorization')
	response_object = {
		'status': 'fail',
		'message': 'Provide a valid auth token.'
	}
	if auth_header:
		auth_token = auth_header.split(' ')[1]
		resp = User.decode_auth_token(auth_token)
		if not isinstance(resp, str):
			user = User.query.filter_by(id=resp).first()
			response_object = {
				'status': 'success',
				'message': 'Success.',
				'data': user.to_json()
			}
			return jsonify(response_object), 200
		else:
			response_object['message'] = resp
			return jsonify(response_object), 401
	else:
		return jsonify(response_object), 403