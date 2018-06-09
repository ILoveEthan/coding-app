import unittest

from sqlalchemy import exc

from project import db
from project.api.models import User

from project.tests.base import BaseTestCase
from project.tests.utils import add_user

class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user(
            username='test',
            email='test@test.com',
            password='randompassword'
        )
        self.assertTrue(user.id)
        self.assertTrue(user.username, 'test')
        self.assertTrue(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user(
            username='test',
            email='test@test.com',
            password='randompassword'
        )
        duplicate_user = User(
            username='test',
            email='test1@test.com',
            password='randompassword'
        )
        db.session.add(duplicate_user)
        self.assertRaises(exc.IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user(
            username='test',
            email='test@test.com',
            password='randompassword'
        )
        duplicate_user = User(
            username='test2',
            email='test@test.com',
            password='randompassword'
        )
        db.session.add(duplicate_user)
        self.assertRaises(exc.IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user(
            username='test',
            email='test@test.com',
            password='randompassword'
        )
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_encode_auth_token(self):
    	user = add_user('test', 'test@test.com', 'test')
    	auth_token = user.encode_auth_token(user.id)
    	self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
    	user = add_user('test', 'test@test.com', 'test')
    	auth_token = user.encode_auth_token(user.id)
    	self.assertTrue(isinstance(auth_token, bytes))
    	self.assertEqual(User.decode_auth_token(auth_token), user.id)

if __name__ == '__main__':
    unittest.main()