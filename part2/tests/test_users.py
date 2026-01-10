import unittest
from app import create_app

class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_valid(self):
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Ali",
            "last_name": "Ahmad",
            "email": "ali@test.com"
        })
        self.assertEqual(res.status_code, 201)

    def test_create_user_invalid(self):
        res = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "bad"
        })
        self.assertEqual(res.status_code, 400)
