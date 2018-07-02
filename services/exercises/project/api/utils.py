def ensure_authenticated(token):
	if current_app.config['TESTING']:
		return True
	url = '{0}/auth/status'.format(current_app.config['USERS_SERVICE_URL'])
	bearer = 'Bearer {0}'.format(token)
	headers = {'Authorization': bearer}
	response = requests.get(url, headers=headers)
	data = json.loads(response.text)
	if response.status_code == 200 and data['status'] == 'success' and data['data']['active']:
		return data
	else:
		return False

