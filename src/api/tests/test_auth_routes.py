from django.test import TestCase, Client
from api.models.user import User
import json

class AuthRoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = "/api/auth/register"
        self.login_url = "/api/auth/login"
        self.me_url = "/api/auth/me"

    def test_register_user(self):
        payload = {
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User"
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_login_user(self):
        User.objects.create_user(email="login@example.com", password="password123")
        payload = {
            "email": "login@example.com",
            "password": "password123"
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        return data["access"]

    def test_get_me(self):
        token = self.test_login_user()
        response = self.client.get(
            self.me_url,
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], "login@example.com")
