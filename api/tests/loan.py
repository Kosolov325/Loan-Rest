from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import (
    Loan, 
    LoanType,
)
import json


class LoanSetup(APITestCase):
    @classmethod
    def setUpTestData(cls):
        with open('tests/loan.json', 'r') as file:
            cls.context = json.load(file)

        context = cls.context['setUp']
        generic_type_data = context['generic_type']
        
        cls.user_data = context['user']
        cls.user = User.objects.create_user(**cls.user_data)
        cls.generic_type = LoanType.objects.get(**generic_type_data)

    def setUp(self):
        self.client.login(**self.user_data)


class LoanCreateTestCase(LoanSetup):
    def create_loan(self, data, user=None):
        data['client'] = user.id if user else self.user.id
        return self.client.post('/api/loans/', data)

    def test_create_loan(self):
        context = self.context[self._testMethodName]
        response = self.create_loan(context['data'])
        self.assertEqual(response.status_code, context['response_status'])
        self.assertEqual(response.data['debt'], context['debt'])
        self.assertEqual(Loan.objects.count(), context['count'])
        self.assertEqual(Loan.objects.get().value, context['value'])

    def test_create_loan_for_other_user(self):
        context = self.context[self._testMethodName]
        other_user = User.objects.create_user(**context['other_user'])
        response = self.create_loan(context['data'], other_user)
        self.assertEqual(response.status_code, context['response_status'])


class LoanReadTestCase(LoanSetup):
    def create_loan_for_user(self, user, data):
        data['client'] = user
        return Loan.objects.create(**data)

    def test_view_loan_details(self):
        context = self.context[self._testMethodName]
        loan = self.create_loan_for_user(self.user, context['data'])
        response = self.client.get(f'/api/loans/{loan.id}/')
        self.assertEqual(response.status_code, context['response_status'])
        self.assertEqual(response.data['value'], context['response_data']['value'])

    def test_view_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user = User.objects.create_user(**context['other_user'])
        loan = self.create_loan_for_user(other_user, context['data'])
        response = self.client.get(f'/api/loans/{loan.id}/')
        self.assertEqual(response.status_code, context['response_status'])


class LoanUpdateTestCase(LoanSetup):
    def test_edit_loan(self):
        context = self.context[self._testMethodName]
        loan = Loan.objects.create(client=self.user, type=self.generic_type, **context['data'])
        response = self.client.patch(f'/api/loans/{loan.id}/', context['data'])
        self.assertEqual(response.status_code, context['response_status'])

    def test_update_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user = User.objects.create_user(**context['other_user'])
        loan = Loan.objects.create(client=other_user, type=self.generic_type, **context['other_loan'])
        response = self.client.patch(f'/api/loans/{loan.id}/', context['data'])
        self.assertEqual(response.status_code, context['response_status'])


class LoanDeleteTestCase(LoanSetup):
    def test_delete_loan(self):
        context = self.context[self._testMethodName]
        loan = Loan.objects.create(client=self.user, **context['data'])
        response = self.client.delete(f'/api/loans/{loan.id}/')
        self.assertEqual(response.status_code, context['response_status'])

    def test_delete_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user = User.objects.create_user(**context['other_user'])
        loan = Loan.objects.create(client=other_user, **context['other_loan'])
        response = self.client.delete(f'/api/loans/{loan.id}/')
        self.assertEqual(response.status_code, context['response_status'])