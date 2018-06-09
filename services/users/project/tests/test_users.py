import json
import unittest

from project.tests.base import BaseTestCase
from project.api.models import User
from project import db

class TestUserService(BaseTestCase):
	def test_users(self):
		response = self.client.get('/users/ping')
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)
		self.assertIn('pong!', data['message'])
		self.assertIn('success', data['status'])


	def test_add_user(self):
		with self.client:
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test',
					'email': 'test@gmail.com',
					'password': 'randompassword'
				}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 201)
			self.assertIn('success', data['status'])
			self.assertIn('test@gmail.com was added!', data['message'])


	def test_add_user_invalid_json(self):
		with self.client:
			response = self.client.post(
				'/users',
				data=json.dumps({}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Invalid payload', data['message'])


	def test_add_user_invalid_json_keys(self):
		with self.client:
			response = self.client.post(
				'/users',
				data=json.dumps({
					'email': 'test@gmail.com'
				}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Invalid payload', data['message'])


	def test_add_user_invalid_json_keys_no_password(self):
		with self.client:
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test',
					'email': 'test@gmail.com'
				}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Invalid payload', data['message'])


	def test_add_user_duplicate_email(self):
		with self.client:
			self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test',
					'email': 'test@gmail.com',
					'password': 'randompassword',
				}),
				content_type='application/json',
			)
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test2',
					'email': 'test@gmail.com',
					'password': 'randompassword',
				}),
				content_type='application/json',
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Sorry. That email already exists.', data['message'])


	def test_single_user(self):
		user = User(username='test', email='test@gmail.com', password='randompassword')
		db.session.add(user)
		db.session.commit()
		with self.client:
			response = self.client.get(f'/users/{user.id}')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertIn('test', data['data']['username'])
			self.assertIn('test@gmail.com', data['data']['email'])
			self.assertIn('success', data['status'])


if __name__ == '__main__':
	unittest.main()