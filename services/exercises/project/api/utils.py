import json
import requests
from functools import wraps
from flask import request, jsonify, current_app

def ensure_authenticated(token):
	if current_app.config['TESTING']:
		test_response = {
			'data': {'id': 999999},
			'status': 'success',
			'admin': True
		}
		return test_response
	url = '{0}/auth/status'.format(current_app.config['USERS_SERVICE_URL'])
	bearer = 'Bearer {0}'.format(token)
	headers = {'Authorization': bearer}
	response = requests.get(url, headers=headers)
	data = json.loads(response.text)
	if response.status_code == 200 and data['status'] == 'success' and data['data']['active']:
		return data
	else:
		return False



def authenticate(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		response_object = {
			'status': 'fail',
			'message': 'Provide a valid auth token.'
		}
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return jsonify(response_object), 403
		auth_token = auth_header.split(' ')[1]
		resp = ensure_authenticated(auth_token)
		if not resp:
			return jsonify(response_object), 401
		return f(resp, *args, **kwargs)

	return decorated_function