from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import LoanType
import json


class LoanTypeSetup(APITestCase):
    @classmethod
    def setUpTestData(cls):
        with open('tests/loantype.json', 'r') as file:
            cls.context = json.load(file)

        context = cls.context['setUp']
        
        cls.user_data = context['user']
        cls.user = User.objects.create_user(**cls.user_data)

    def setUp(self):
        self.client.login(**self.user_data)

class LoanTypeCreateTestCase(LoanTypeSetup):
    def create_loan_type(self, data, user=None):
        data['client'] = user.id if user else self.user.id
        return self.client.post('/api/loans/types/', data)

    def test_create_loan_type(self):
        context = self.context[self._testMethodName]
        response = self.create_loan_type(context['data'])
        self.assertEqual(response.status_code, context['response_status'])
    
    def test_create_loan_type_non_staff(self):
        context = self.context[self._testMethodName]
        user_data = context['user']
        User.objects.create_user(**user_data)
        self.client.login(**user_data)
        response = self.create_loan_type(context['data'])
        self.assertEqual(response.status_code, context['response_status'])
    
    def test_create_loan_type_factor_less_than_zero(self):
        context = self.context[self._testMethodName]
        response = self.create_loan_type(context['data'])
        self.assertEqual(response.status_code, context['response_status'])


class LoanTypeRetrieveTestCase(LoanTypeSetup):
    def test_get_loan_type(self):
        context = self.context[self._testMethodName]
        loan_type = LoanType.objects.create(**context['loan_type'])
        response = self.client.get(f'/api/loans/types/{loan_type.id}/')
        self.assertEqual(response.status_code, context['response_status'])
        self.assertEqual(response.data['name'], context['response_data']['name'])


class LoanTypeUpdateTestCase(LoanTypeSetup):
    def update_loan_type(self, loan_type_id, data):
        return self.client.patch(f'/api/loans/types/{loan_type_id}/', data)

    def test_update_loan_type(self):
        context = self.context[self._testMethodName]
        loan_type = LoanType.objects.create(**context['loan_type'])
        response = self.update_loan_type(loan_type.id, context['new_data'])
        self.assertEqual(response.status_code, context['response_status'])
        self.assertEqual(LoanType.objects.get(id=loan_type.id).factor, context['new_data']['factor'])

    def test_update_loan_type_non_staff(self):
        context = self.context[self._testMethodName]
        loan_type = LoanType.objects.create(**context['loan_type'])
        user_data = context['user']
        User.objects.create_user(**user_data)
        self.client.login(**user_data)
        response = self.update_loan_type(loan_type.id, context['new_data'])
        self.assertEqual(response.status_code, context['response_status'])


class LoanTypeDeleteTestCase(LoanTypeSetup):
    def test_delete_loan_type(self):
        context = self.context[self._testMethodName]
        loan_type = LoanType.objects.create(**context['loan_type'])
        response = self.client.delete(f'/api/loans/types/{loan_type.id}/')
        self.assertEqual(response.status_code, context['response_status'])

    def test_delete_loan_type_non_staff(self):
        context = self.context[self._testMethodName]
        loan_type = LoanType.objects.create(**context['loan_type'])
        user_data = context['user']
        User.objects.create_user(**user_data)
        self.client.login(**user_data)
        response = self.client.delete(f'/api/loans/types/{loan_type.id}/')
        self.assertEqual(response.status_code, context['response_status'])