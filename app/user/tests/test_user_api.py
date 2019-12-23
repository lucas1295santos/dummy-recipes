from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(params)


# This public one is for requests that dont need to be authenticated
class PublicUserAPITests(TestCase):
    """Tests user public apis"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'superpassword',
            'name': 'Test Case'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # This gets an dictionary from the response, and parses each field as
        # an parameter to get
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        # Assert that the password is not returned on the response
        # for obvious security matters
        self.assertNotIn('password', response.data)
        self.assertEqual(user.name, payload['name'])
        self.assertEqual(user.email, payload['email'])

    def test_creat_duplicated_user(self):
        """Test creating an User that already exists"""
        payload = {
            'email': 'test@test.com',
            'password': 'superpassword'
        }
        create_user(**payload)  # Creates first user
        # Request creation of second user
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Tests password have to be at least 8 chars long"""

        payload = {
            'email': 'test@test.com',
            'password': 'pwd'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertTrue(response.status_code, status.HHTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)