from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_superuser_sets_staff_and_superuser_flags(self):
        User = get_user_model()

        user = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
