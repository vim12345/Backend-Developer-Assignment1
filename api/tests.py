from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Paragraph

class APITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)

        # Create a test paragraph
        self.test_paragraph_content = "This is a test paragraph."
        self.test_paragraph = Paragraph.objects.create(content=self.test_paragraph_content)

    def test_user_registration(self):
        url = '/api/register/'
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_id', response.data)
        self.assertIn('token', response.data)

    def test_user_login(self):
        url = '/api/login/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)
        self.assertIn('token', response.data)

    def test_search_paragraph(self):
        url = '/api/search/'
        search_word = 'test'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(f'{url}?word={search_word}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.test_paragraph_content)

    def test_search_paragraph_without_authentication(self):
        url = '/api/search/'
        search_word = 'test'

        response = self.client.get(f'{url}?word={search_word}')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
