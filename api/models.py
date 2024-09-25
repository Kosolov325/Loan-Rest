from decimal import Decimal
from datetime import date
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class LoanType(models.Model):
    name = models.CharField(max_length=255)
    factor = models.DecimalField(max_digits=20, decimal_places=5, default=0.0)

    class Meta:
        verbose_name = 'Loan Type'
        verbose_name_plural = 'Loan Types'
        db_table = 'loan_types'

    def __str__(self):
        return self.name
    

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(LoanType, on_delete=models.SET_NULL, null=True, related_name="type")
    ip_address = models.GenericIPAddressField()
    date = models.DateField(auto_now_add=True)
    bank = models.CharField(max_length=255)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")

    @property
    def debt(self):
        payments = self.payments.aggregate(total=Sum('amount'))['total'] or 0  # Somar diretamente na database para melhor performance
        pro_rata = Decimal((1 + self.type.factor / 100)) ** (date.today() - self.date).days
        return (self.value * pro_rata) - payments

    class Meta:
        verbose_name = 'loan'
        verbose_name_plural = 'Loans'
        db_table = 'loans'

    def __str__(self):
        return f"{self.id}"


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'Payments'
        db_table = 'payments'

    def __str__(self):
        return f"{self.id}"
