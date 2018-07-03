import json
import unittest

from project.tests.base import BaseTestCase
from project.api.models import User
from project import db
from project.tests.utils import add_user

class TestUserService(BaseTestCase):
	def test_users(self):
		response = self.client.get('/users/ping')
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)
		self.assertIn('pong!', data['message'])
		self.assertIn('success', data['status'])


	def test_add_user(self):
		add_user('random', 'random@random', 'random')
		user = User.query.filter_by(email='random@random').first()
		user.admin = True
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'random@random',
					'password': 'random'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test',
					'email': 'test@gmail.com',
					'password': 'randompassword'
				}),
				content_type='application/json',
				headers={'Authorization': f'Bearer {token}'}
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 201)
			self.assertIn('success', data['status'])
			self.assertIn('test@gmail.com was added!', data['message'])


	def test_add_user_invalid_json(self):
		add_user('random', 'random@random', 'random')
		user = User.query.filter_by(email='random@random').first()
		user.admin = True
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'random@random',
					'password': 'random'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			response = self.client.post(
				'/users',
				data=json.dumps({}),
				content_type='application/json',
				headers={'Authorization': f'Bearer {token}'}
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Invalid payload', data['message'])


	def test_add_user_invalid_json_keys(self):
		add_user('random', 'random@random', 'random')
		user = User.query.filter_by(email='random@random').first()
		user.admin = True
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'random@random',
					'password': 'random'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			response = self.client.post(
				'/users',
				data=json.dumps({
					'email': 'test@gmail.com'
				}),
				content_type='application/json',
				headers={'Authorization': f'Bearer {token}'}
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Invalid payload', data['message'])


	def test_add_user_invalid_json_keys_no_password(self):
		add_user('random', 'random@random', 'random')
		user = User.query.filter_by(email='random@random').first()
		user.admin = True
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'random@random',
					'password': 'random'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test',
					'email': 'test@gmail.com'
				}),
				content_type='application/json',
				headers={'Authorization': f'Bearer {token}'}
			)
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', data['status'])
			self.assertIn('Invalid payload', data['message'])


	def test_add_user_duplicate_email(self):
		add_user('random', 'random@random', 'random')
		user = User.query.filter_by(email='random@random').first()
		user.admin = True
		db.session.commit()
		with self.client:
			resp_login = self.client.post(
				'/auth/login',
				data=json.dumps({
					'email': 'random@random',
					'password': 'random'
				}),
				content_type='application/json'
			)
			token = json.loads(resp_login.data.decode())['auth_token']
			self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test',
					'email': 'test@gmail.com',
					'password': 'randompassword',
				}),
				content_type='application/json',
				headers={'Authorization': f'Bearer {token}'}
			)
			response = self.client.post(
				'/users',
				data=json.dumps({
					'username': 'test2',
					'email': 'test@gmail.com',
					'password': 'randompassword',
				}),
				content_type='application/json',
				headers={'Authorization': f'Bearer {token}'}
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