from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Gera usuários rapidamente"

    def add_arguments(self, parser):
        parser.add_argument('-u', type=str, help='Nome de usuário do cliente')
        parser.add_argument('-p', type=str, help='Senha do cliente')

    def handle(self, *args, **kwargs):
        username = kwargs['u']
        password = kwargs['p']

        if not username or not password:
            self.stdout.write(self.style.ERROR("Você deve fornecer um nome de usuário e uma senha."))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"Usuário '{username}' já existe."))
            return

        user = User.objects.create_user(username=username, password=password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Usuário '{username}' criado com sucesso."))