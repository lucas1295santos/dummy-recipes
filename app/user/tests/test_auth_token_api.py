from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class AuthTokenAPITests(TestCase):
    """Test public api test for creating an auth token"""

    def test_create_token_for_user(self):
        """Test that a token is created for an user"""
        payload = {
            'email': 'test@test.com',
            'password': 'somepassword',
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_token_with_invalid_credentials(self):
        """Test that no token is generated for invalid credentials"""
        payload = {
            'email': 'test@test.com',
            'passowrd': 'wrongpassword',
        }
        create_user(email='test@test.com', password='somepassword')
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_with_no_user(self):
        """Test that no token is generated if user does not exist"""
        payload = {
            'email': 'test@test.com',
            'passowrd': 'somepassword',
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_missing_password(self):
        """Test that a password is required"""
        payload = {
            'email': 'test@test.com',
            'passowrd': '',
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
