import json
import unittest

from project.tests.base import BaseTestCase
from project.api.models import User
from project import db
from project.tests.utils import add_user

class testAuthBlueprint(BaseTestCase):
	def test_user_registration(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({
					'username': 'test',
					'email': 'test@test.com',
					'password': '123456',
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(data['status'], 'success')
			self.assertEqual(data['message'], 'Successfully registered.')
			self.assertTrue(data['auth_token'])
			self.assertEqual(response.content_type, 'application/json')
			self.assertEqual(response.status_code, 201)

	def test_user_registration_duplicate_username(self):
		add_user('test', 'test@test.com', '123456')
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({
					'username': 'test',
					'email': 'test1@test.com',
					'password': '123456',
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertEqual(data['message'], 'Sorry. That user already exists.')
			self.assertEqual(data['status'], 'fail')

	def test_user_registration_duplicate_email(self):
		add_user('test', 'test@test.com', '123456')
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({
					'username': 'test1',
					'email': 'test@test.com',
					'password': '123456',
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertEqual(data['message'], 'Sorry. That user already exists.')
			self.assertEqual(data['status'], 'fail')

	def test_user_registration_invalid_json(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertEqual(data['message'], 'Invalid payload.')
			self.assertEqual(data['status'], 'fail')

	def test_user_registration_invalid_json_keys_no_username(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({
					'email': 'test@test.com',
					'password': '123456',
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertEqual(data['message'], 'Invalid payload.')
			self.assertEqual(data['status'], 'fail')

	def test_user_registration_invalid_json_keys_no_email(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({
					'username': 'test',
					'password': '123456',
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertEqual(data['message'], 'Invalid payload.')
			self.assertEqual(data['status'], 'fail')

	def test_user_registration_invalid_json_keys_no_password(self):
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps({
					'username': 'test',
					'email': 'test@test.com',
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertEqual(data['message'], 'Invalid payload.')
			self.assertEqual(data['status'], 'fail')

	def test_registered_user_login(self):
		with self.client:
			add_user('test', 'test@test.com', '123456')
			response = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'test@test.com',
					'password': '123456'
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(data['status'], 'success')
			self.assertEqual(data['message'], 'Successfully logged in.')
			self.assertEqual(response.content_type, 'application/json')
			self.assertTrue(data['auth_token'])

	def test_not_registered_user_login(self):
		with self.client:
			response = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'test@test.com',
					'password': '123456'
				}),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 404)
			self.assertEqual(data['status'], 'fail')
			self.assertEqual(data['message'], 'User does not exist.')
			self.assertEqual(response.content_type, 'application/json')

	def test_valid_logout(self):
		add_user('test', 'test@test.com', '123456')
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'test@test.com',
					'password': '123456'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			response = self.client.get(
				'/auth/logout',
				headers={'Authorization': f'Bearer {token}'}
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(data['status'], 'success')
			self.assertEqual(data['message'], 'Successfully logged out.')

	def test_invalid_logout(self):
		pass

	def test_invalid_logout_expired_token(self):
		pass

	def test_user_status(self):
		add_user('test', 'test@test.com', '123456')
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'test@test.com',
					'password': '123456'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			response = self.client.get(
				'/auth/status',
				headers={'Authorization': f'Bearer {token}'}
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(data['status'], 'success')
			self.assertEqual(data['message'], 'Success.')
			self.assertEqual(data['data']['username'], 'test')
			self.assertEqual(data['data']['email'], 'test@test.com')
			self.assertTrue(data['data']['active'] is True)


	def test_invalid_user_status(self):
		pass


if __name__ == '__main__':
	unittest.main()
