import json
import unittest

from project.tests.base import BaseTestCase
#from project.api.models import User
#from project import db

class TestUserService(BaseTestCase):
	def test_users(self):
		response = self.client.get('/exercises/ping')
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)
		self.assertIn('pong!', data['message'])
		self.assertIn('success', data['status'])
