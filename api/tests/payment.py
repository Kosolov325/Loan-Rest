from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import (
    LoanType, 
    Loan, 
    Payment,
)
import json

class PaymentSetup(APITestCase):

    @classmethod
    def setUpTestData(cls):
        with open('tests/payment.json', 'r') as file:
            cls.context = json.load(file)

        context = cls.context['setUp']
        generic_type_data = context['generic_type']
        loan_data = context['loan']
        cls.user_data = context['user']
        cls.user = User.objects.create_user(**cls.user_data)
        cls.generic_type = LoanType.objects.get(**generic_type_data)     
        loan_data['client'] = cls.user
        loan_data['type'] = cls.generic_type
        cls.loan = Loan.objects.create(**loan_data)

    def setUp(self):
        self.client.login(**self.user_data)


class PaymentCreateTestCase(PaymentSetup):
    def create_payment(self, data, loan=None):
        data['loan'] = loan.id if loan else self.loan.id
        return self.client.post('/api/payments/', data)

    def test_create_payment(self):
        context = self.context[self._testMethodName]
        response = self.create_payment(context['data'])
        self.assertEqual(response.status_code, context['response_status'])
        self.assertEqual(Payment.objects.count(), context['count'])
        self.assertEqual(Payment.objects.get().amount, context['amount'])

    def test_create_payment_for_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user_data = context['other_user']
        other_user = User.objects.create_user(**other_user_data)
        other_loan_data = context['other_loan']
        other_loan_data['type'] = self.generic_type
        other_loan_data['client'] = other_user
        other_loan = Loan.objects.create(**other_loan_data)
        response = self.create_payment(context['data'], other_loan)
        self.assertEqual(response.status_code, context['response_status'])

    def test_create_payment_greater_loan_debt(self):
        context = self.context[self._testMethodName]
        response = self.create_payment(context['data'])
        self.assertEqual(response.status_code, context['response_status'])

    def test_create_payment_negative_amount(self):
        context = self.context[self._testMethodName]
        response = self.create_payment(context['data'])
        self.assertEqual(response.status_code, context['response_status'])

class PaymentReadTestCase(PaymentSetup):
    def test_view_payment(self):
        context = self.context[self._testMethodName]
        payment = Payment.objects.create(loan=self.loan, **context['data'])
        response = self.client.get(f'/api/payments/{payment.id}/')
        self.assertEqual(response.status_code, context['response_status'])

    def test_view_payment_for_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user_data = context['other_user']
        other_user = User.objects.create_user(**other_user_data)
        other_loan_data = context['other_loan']
        other_loan_data['type'] = self.generic_type
        other_loan_data['client'] = other_user
        other_loan = Loan.objects.create(**other_loan_data)
        payment = Payment.objects.create(loan=other_loan, **context['data'])
        response = self.client.get(f'/api/payments/{payment.id}/')
        self.assertEqual(response.status_code, context['response_status'])


class PaymentUpdateTestCase(PaymentSetup):
    def test_edit_payment(self):
        context = self.context[self._testMethodName]
        payment = Payment.objects.create(loan=self.loan, **context['data'])
        response = self.client.patch(f'/api/payments/{payment.id}/', context['new_data'])
        self.assertEqual(response.status_code, context['response_status'])

    def test_edit_payment_for_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user_data = context['other_user']
        other_user = User.objects.create_user(**other_user_data)
        other_loan_data = context['other_loan']
        other_loan_data['type'] = self.generic_type
        other_loan_data['client'] = other_user
        other_loan = Loan.objects.create(**other_loan_data)
        payment = Payment.objects.create(loan=other_loan, **context['other_payment'])
        response = self.client.patch(f'/api/payments/{payment.id}/', context['new_data'])
        self.assertEqual(response.status_code, context['response_status'])


class PaymentDeleteTestCase(PaymentSetup):
    def test_delete_payment(self):
        context = self.context[self._testMethodName]
        payment = Payment.objects.create(loan=self.loan, **context['data'])
        response = self.client.delete(f'/api/payments/{payment.id}/')
        self.assertEqual(response.status_code, context['response_status'])

    def test_delete_payment_for_other_user_loan(self):
        context = self.context[self._testMethodName]
        other_user_data = context['other_user']
        other_user = User.objects.create_user(**other_user_data)
        other_loan_data = context['other_loan']
        other_loan_data['type'] = self.generic_type
        other_loan_data['client'] = other_user
        other_loan = Loan.objects.create(**other_loan_data)
        payment = Payment.objects.create(loan=other_loan, **context['other_payment'])
        response = self.client.delete(f'/api/payments/{payment.id}/')
        self.assertEqual(response.status_code, context['response_status'])