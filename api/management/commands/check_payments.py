from django.core.management.base import BaseCommand
from api.models import Payment
import csv

class Command(BaseCommand):
    help = "Gera um CSV contendo pagamentos irregulares."
    header = ["ID", "Valor", "Empréstimo", "Cliente", "Valor Empréstimo", "Dívida", "Data Pagamento"]

    def add_arguments(self, parser):
        parser.add_argument('-o', type=str, help='Local do arquivo CSV de saída')

    def handle(self, *args, **kwargs):
        output_file = kwargs['o'] or 'pagamentos_irregulares.csv'

        payments = []
        for payment in Payment.objects.all():
            loan = payment.loan
            if payment.amount < 0 or payment.amount > loan.debt:
                payments.append([
                    payment.id, 
                    payment.amount, 
                    loan.id, 
                    loan.client.username, 
                    loan.value, 
                    loan.debt, 
                    payment.date
                ])

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            writer.writerows(payments)

        self.stdout.write(self.style.SUCCESS(f"CSV gerado com sucesso em {output_file}"))
