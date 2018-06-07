from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from project.api.models import User
from project import db

bp = Blueprint('users', __name__)

@bp.route('/users/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong!'
	})

@bp.route('/users', methods=['POST'])
def add_user():
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
		user = User.query.filter_by(email=email).first()
		if not user:
			db.session.add(User(username=username, email=email, password=password))
			db.session.commit()
			response_object = {
				'status': 'success',
				'message': f'{email} was added!'
			}
			return jsonify(response_object), 201
		else:
			response_object = {
				'status': 'fail',
				'message': 'Sorry. That email already exists.'
			}
			return jsonify(response_object), 400
	except (exc.IntegrityError, TypeError) as e:
		db.session.rollback()
		return jsonify(response_object), 400


@bp.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
	user = User.query.filter_by(id=int(user_id)).first()
	response_object = {
		'status': 'success',
		'data': user.to_json()
	}
	return jsonify(response_object), 200

@bp.route('/users', methods=['GET'])
def get_all_users():
	users = User.query.all()
	response_object = {
		'status': 'success',
		'data': {
			'users': [user.to_json() for user in users]
		}
	}
	return jsonify(response_object), 200