from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import Message


class Command(BaseCommand):
    help = 'Limpa todos os usuários e cria apenas gabi e leo com senha borlaria'

    def handle(self, *args, **options):
        # Deletar todas as mensagens
        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Mensagens deletadas'))

        # Deletar todos os usuários exceto superusuários
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('Usuários não-superusuários deletados'))

        # Criar usuário gabi
        if not User.objects.filter(username='gabi').exists():
            gabi = User.objects.create_user(
                username='gabi',
                password='borlaria'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuário "gabi" criado'))
        else:
            gabi = User.objects.get(username='gabi')
            gabi.set_password('borlaria')
            gabi.save()
            self.stdout.write(self.style.SUCCESS(f'Senha do usuário "gabi" atualizada'))

        # Criar usuário leo
        if not User.objects.filter(username='leo').exists():
            leo = User.objects.create_user(
                username='leo',
                password='borlaria'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuário "leo" criado'))
        else:
            leo = User.objects.get(username='leo')
            leo.set_password('borlaria')
            leo.save()
            self.stdout.write(self.style.SUCCESS(f'Senha do usuário "leo" atualizada'))

        self.stdout.write(self.style.SUCCESS('\n✅ Setup concluído!'))
        self.stdout.write(self.style.SUCCESS('Usuários criados:'))
        self.stdout.write(self.style.SUCCESS('  - gabi (senha: borlaria)'))
        self.stdout.write(self.style.SUCCESS('  - leo (senha: borlaria)'))
