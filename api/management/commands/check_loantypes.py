from django.core.management.base import BaseCommand
from api.models import LoanType
import csv

class Command(BaseCommand):
    help = "Gera um CSV contendo tipos de empréstimos irregulares."
    header = ["ID", "Nome", "Fator"]

    def add_arguments(self, parser):
        parser.add_argument('-o', type=str, help='Local do arquivo CSV de saída')

    def handle(self, *args, **kwargs):
        output_file = kwargs['o'] or 'tipos_emprestimos_irregulares.csv'

        ltypes = LoanType.objects.filter(factor__lt=0)
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            for ltype in ltypes:
                writer.writerow([ltype.id, ltype.name, ltype.factor])

        self.stdout.write(self.style.SUCCESS(f"CSV gerado com sucesso em {output_file}"))