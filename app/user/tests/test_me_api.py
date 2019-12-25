from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class MeAPITests(TestCase):
    """Tests me api"""

    def setUp(self):
        self.unauthenticatedClient = APIClient()
        self.user = create_user(
            email='test@test.com',
            password='somepassword',
            name='test user',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_me_failure(self):
        """Assert that me requires authentication"""
        response = self.unauthenticatedClient.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_success(self):
        """Assert that it is possible to retrieve an user profile"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_to_me_is_not_allowed(self):
        """Assert that POST is not allowed on me endpoint"""
        response = self.client.post(ME_URL, {})

        expected_status = status.HTTP_504_METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, expected_status)

    def test_patch_user_profile(self):
        """Test updating an authenticated user via patch"""
        payload = {
            'name': 'new name',
            'password': 'newpassword',
        }
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
