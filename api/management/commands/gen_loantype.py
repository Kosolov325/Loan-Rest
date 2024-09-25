from django.core.management.base import BaseCommand
from api.models import LoanType
from decimal import Decimal

class Command(BaseCommand):
    help = "Gera tipos de empréstimos rapidamente"

    def add_arguments(self, parser):
        parser.add_argument('-n', type=str, help='Nome do tipo de empréstimo')
        parser.add_argument('-f', type=Decimal, help='Fator de juros do tipo de empréstimo')

    def handle(self, *args, **kwargs):
        nome = kwargs['n']
        fator = kwargs['f']

        _, created = LoanType.objects.get_or_create(name=nome, factor=fator)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Tipo de empréstimo {nome} criado com sucesso"))
        else:
            self.stdout.write(self.style.WARNING(f"Tipo de empréstimo {nome} já existe"))