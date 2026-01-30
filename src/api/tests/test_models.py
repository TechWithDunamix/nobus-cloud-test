from django.test import TestCase
from api.models.user import User
from api.models.loan_application import LoanApplication, LoanStatus
from api.models.admin_log import AdminLog

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", password="password123")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(str(user), "test@example.com")

class LoanApplicationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="loaner@example.com", password="password")

    def test_create_loan(self):
        loan = LoanApplication.objects.create(
            user=self.user,
            amount=5000.00,
            tenure_months=12,
            purpose="Business"
        )
        self.assertEqual(loan.status, LoanStatus.PENDING)
        self.assertEqual(loan.amount, 5000.00)
        self.assertTrue("Loan" in str(loan))

class AdminLogModelTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email="admin@example.com", password="password")
        self.admin.is_staff = True
        self.admin.save()

    def test_create_log(self):
        log = AdminLog.objects.create(
            admin=self.admin,
            action="TEST_ACTION",
            target_id=1,
            target_model="TestModel"
        )
        self.assertEqual(log.admin, self.admin)
        self.assertEqual(log.action, "TEST_ACTION")
