from django.core.management.base import BaseCommand
from api.models import (
    Payment, 
    Loan,
)
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = "Gera pagamentos rapidamente"

    def add_arguments(self, parser):
        parser.add_argument('-l', type=str, help='UUID do empréstimo')
        parser.add_argument('-a', type=Decimal, help='Valor do pagamento')

    def handle(self, *args, **kwargs):
        loan_id = kwargs['l']
        amount = kwargs['a']

        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Emprestimo fornecido inexistente"))
            return

        Payment.objects.create(
            loan=loan,
            amount=amount,
            date=date.today()
        )

        self.stdout.write(self.style.SUCCESS(f"Pagamento de R$ {amount} registrado para o empréstimo {loan_id} com sucesso"))