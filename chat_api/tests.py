# chat_api/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User, Chat

class ChatAPITests(APITestCase):

    def setUp(self):
        self.user_data = {'username': 'testuser', 'password': 'strongpassword123'}
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_user_registration_success(self):
        # Use the namespaced URL
        url = reverse('chat_api:register')
        data = {'username': 'newuser', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertIn('token', response.data)

    def test_user_registration_duplicate_username(self):
        # Use the namespaced URL
        url = reverse('chat_api:register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        # Use the namespaced URL
        url = reverse('chat_api:Login')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_wrong_password(self):
        # Use the namespaced URL
        url = reverse('chat_api:Login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_chat_api_success(self):
        # Use the namespaced URL
        url = reverse('chat_api:Chat')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        initial_tokens = self.user.tokens
        response = self.client.post(url, {'message': 'Hello world'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('response', response.data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.tokens, initial_tokens - 10)
        self.assertEqual(Chat.objects.count(), 1)

    def test_chat_api_insufficient_tokens(self):
        self.user.tokens = 50
        self.user.save()
        # Use the namespaced URL
        url = reverse('chat_api:Chat')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url, {'message': 'Hello again'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_chat_api_unauthenticated(self):
        # Use the namespaced URL
        url = reverse('chat_api:Chat')
        response = self.client.post(url, {'message': 'Trying to sneak in'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_balance_api_success(self):
        # Use the namespaced URL
        url = reverse('chat_api:Token Balance')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tokens'], self.user.tokens)

    def test_token_balance_api_unauthenticated(self):
        # Use the namespaced URL
        url = reverse('chat_api:Token Balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)