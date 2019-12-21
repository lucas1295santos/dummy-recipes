from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_email_password_success(self):
        """Test if creating an user is successful"""
        email = 'user@dummy.com'
        password = 'Test1234abc'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests if users email is normalized on creation"""
        email = 'user@dumMy.cOm'
        password = 'user@dummy.com'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        expected_normalized_email = 'user@dummy.com'
        self.assertEqual(user.email, expected_normalized_email)

    def test_new_user_invalid_email(self):
        """Tests if user email is validated on creation"""
        with self.assertRaises(ValueError):
            password = 'test123'
            user = get_user_model().objects.create_user(
                email=None,
                password=password
            )
