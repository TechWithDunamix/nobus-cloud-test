from django.test import TestCase, Client
from api.models.user import User
from api.models.loan_application import LoanApplication
from api.services.jwt_service import JWTService
import json

class LoanRoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="loanuser@example.com", password="password")
        self.token = JWTService.create_access_token(self.user.id, self.user.email)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        self.loans_url = "/api/loans/"

    def test_create_loan(self):
        payload = {
            "amount": 5000.00,
            "tenure_months": 24,
            "purpose": "Education"
        }
        response = self.client.post(
            self.loans_url,
            data=json.dumps(payload),
            content_type="application/json",
            **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoanApplication.objects.count(), 1)
        self.assertEqual(LoanApplication.objects.first().user, self.user)

    def test_list_loans(self):
        LoanApplication.objects.create(user=self.user, amount=1000, tenure_months=12, purpose="Test")
        response = self.client.get(self.loans_url, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
