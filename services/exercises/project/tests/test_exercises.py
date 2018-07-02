import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_exercise
from project.api.models import Exercise
from project import db

class TestExercisesService(BaseTestCase):
	def test_exercises(self):
		response = self.client.get('/exercises/ping')
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)
		self.assertIn('pong!', data['message'])
		self.assertIn('success', data['status'])

	def test_all_exercises(self):
		add_exercise()
		add_exercise('hello world', 'print("Hello, World!")', 'Hello, World!')
		with self.client:
			response = self.client.get('/exercises')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertIn('success', data['status'])
			self.assertEqual(len(data['data']['exercises']), 2)
			self.assertIn(
				'Define a function called sum',
				data['data']['exercises'][0]['body'])
			self.assertEqual(
				'sum(2, 2)',
				data['data']['exercises'][0]['test_code'])
			self.assertEqual(
				'4',
				data['data']['exercises'][0]['test_code_solution'])
			self.assertIn(
				'hello world',
				data['data']['exercises'][1]['body'])
			self.assertEqual(
				'print("Hello, World!")',
				data['data']['exercises'][1]['test_code'])
			self.assertEqual(
				'Hello, World!',
				data['data']['exercises'][1]['test_code_solution'])

	def test_add_exercise(self):
		data = {
			'body': 'hello world', 
			'test_code': 'print("Hello, World!")', 
			'test_code_solution': 'Hello, World!'
		}
		with self.client:
			response = self.client.post(
				'/exercises', 
				data=json.dumps(data),
				content_type='application/json',
				headers=({'Authorization': 'Bearer test'})
			)
			data = json.loads(response.data.decode())
			self.assertEqual(201, response.status_code)
			self.assertEqual('success', data['status'])
			self.assertEqual('New exercise was added!', data['message'])

if __name__ == '__main__':
	unittest.main()
