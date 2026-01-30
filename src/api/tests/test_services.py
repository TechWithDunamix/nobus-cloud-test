from django.test import TestCase
from unittest.mock import patch
from api.models.user import User
from api.services.jwt_service import JWTService
from api.services.email_service import send_loan_approval_email

class JWTServiceTests(TestCase):
    def test_create_and_validate_token(self):
        token = JWTService.create_access_token(user_id=1, email="test@example.com")
        payload = JWTService.validate_access_token(token)
        self.assertEqual(payload['user_id'], 1)
        self.assertEqual(payload['email'], "test@example.com")
        self.assertEqual(payload['type'], 'access')

    def test_refresh_token(self):
        refresh = JWTService.create_refresh_token(user_id=1, email="test@example.com")
        new_access, payload = JWTService.refresh_access_token(refresh)
        self.assertIsNotNone(new_access)
        self.assertEqual(payload['user_id'], 1)

class EmailServiceTests(TestCase):
    @patch('api.services.email_service.send_mail')
    def test_send_approval_email(self, mock_send_mail):
        result = send_loan_approval_email(
            user_email="user@example.com",
            user_name="John Doe",
            amount=1000.00,
            tenure=12
        )
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        args = mock_send_mail.call_args[1]
        self.assertIn("John Doe", args['html_message'])
        self.assertIn("1,000.00", args['html_message'])
