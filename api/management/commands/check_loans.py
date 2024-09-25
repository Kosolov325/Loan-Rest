from django.core.management.base import BaseCommand
from api.models import Loan
from datetime import date
import csv


class Command(BaseCommand):
    help = "Gera um CSV contendo empréstimos irregulares."
    header = ["ID", "Valor", "Cliente", "Data do Empréstimo", "Valor do Débito"]

    def add_arguments(self, parser):
        parser.add_argument('-o', type=str, help='Local do arquivo CSV de saída')

    def handle(self, *args, **kwargs):
        output_file = kwargs['o'] or 'emprestimos_irregulares.csv'

        loans = Loan.objects.all()
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            for loan in loans:
                if loan.debt < 0 or loan.date > date.today():
                    writer.writerow([loan.id, loan.value, loan.client.username, loan.date, loan.debt])

        self.stdout.write(self.style.SUCCESS(f"CSV gerado com sucesso em {output_file}"))
