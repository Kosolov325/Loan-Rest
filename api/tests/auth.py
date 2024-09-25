from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
import json


class AuthTokenTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open('tests/auth.json', 'r') as file:
            cls.context = json.load(file)

    def setUp(self):
        context = self.context['setUp']
        self.user = User.objects.create_user(**context['data'])

    def test_obtain_token(self):
        context = self.context['test_obtain_token']
        data = context['data']
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, context['response_status'])
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        context = self.context['test_refresh_token']
        refresh = RefreshToken.for_user(self.user)
        data = {
            "refresh": str(refresh)
        }
        response = self.client.post('/api/token/refresh/', data)
        self.assertEqual(response.status_code, context['response_status'])
        self.assertIn('access', response.data)

    def test_obtain_token_invalid_credentials(self):
        context = self.context['test_obtain_token_invalid_credentials']
        data = context['data']
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, context['response_status'])

    def test_refresh_token_invalid(self):
        context = self.context['test_refresh_token_invalid']
        data = context['data']
        response = self.client.post('/api/token/refresh/', data)
        self.assertEqual(response.status_code, context['response_status'])

    def test_access_denied_without_token(self):
        context = self.context[self._testMethodName]
        self.client.logout()
        types = self.client.get('/api/loans/types/')
        loans = self.client.get('/api/loans/')
        payments = self.client.get('/api/payments/')
        self.assertEqual(types.status_code, context['response_status'])
        self.assertEqual(loans.status_code, context['response_status'])
        self.assertEqual(payments.status_code, context['response_status'])