from django.core.management.base import BaseCommand
from api.models import Loan, LoanType
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = "Gera empréstimos rapidamente"

    def add_arguments(self, parser):
        parser.add_argument('-u', type=int, help='ID do cliente')
        parser.add_argument('-a', type=Decimal, help='Valor do empréstimo')
        parser.add_argument('-t', type=int, help='ID do tipo de empréstimo')

    def handle(self, *args, **kwargs):
        user = kwargs['u']
        valor = kwargs['a']
        loan_type_id = kwargs['t']

        try:
            user = User.objects.get(id=user)
            loan_type = LoanType.objects.get(id=loan_type_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Usuário fornecido inexistente"))
            return
        except LoanType.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Emprestimo fornecido inexistente"))
            return

        Loan.objects.create(
            client=user,
            value=valor,
            type=loan_type,
            date=date.today(),
            ip_address='127.0.0.1',
            bank='Banco Automático'
        )

        self.stdout.write(self.style.SUCCESS(f"Empréstimo de R$ {valor} criado para {user.username} com sucesso"))