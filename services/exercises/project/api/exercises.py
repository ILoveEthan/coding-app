from flask import Blueprint, jsonify, request

bp = Blueprint('exercises', __name__)

@bp.route('/exercises/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong!'
	})