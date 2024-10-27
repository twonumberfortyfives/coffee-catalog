from django.test import TestCase
from rest_framework.test import APIClient

from user.models import User


class UserUnauthorizedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test_passWOrd1",
        )
        self.client.force_authenticate(user=self.user)

    def test_email_not_verified(self):
        self.assertEqual(self.user.is_verified, False)
