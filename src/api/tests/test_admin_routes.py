from django.test import TestCase, Client
from unittest.mock import patch
from api.models.user import User
from api.models.loan_application import LoanApplication, LoanStatus
from api.models.admin_log import AdminLog
from api.services.jwt_service import JWTService
import json

class AdminRoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(email="admin@example.com", password="password")
        self.admin.is_staff = True
        self.admin.save()
        self.token = JWTService.create_access_token(self.admin.id, self.admin.email)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        
        self.user = User.objects.create_user(email="user@example.com", password="password")
        self.loan = LoanApplication.objects.create(
            user=self.user, amount=1000, tenure_months=12, purpose="Test"
        )
        self.admin_loans_url = "/api/admin/loans"

    def test_list_all_loans(self):
        response = self.client.get(self.admin_loans_url, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    @patch('api.services.email_service.send_loan_approval_email')
    def test_approve_loan(self, mock_email):
        url = f"/api/admin/loans/{self.loan.id}/status"
        payload = {"status": "APPROVED", "reason": "Looks good"}
        
        response = self.client.put(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            **self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, LoanStatus.APPROVED)
        
       
        
        # Verify Log Created
        self.assertTrue(AdminLog.objects.filter(target_id=self.loan.id, action="APPROVED_LOAN").exists())
