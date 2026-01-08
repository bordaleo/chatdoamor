from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import Message


class Command(BaseCommand):
    help = 'Limpa todos os usuários e cria apenas gabi e leo com senha borlaria'

    def handle(self, *args, **options):
        self.stdout.write('🗑️  Deletando todas as mensagens...')
        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✅ Mensagens deletadas'))

        self.stdout.write('🗑️  Deletando usuários não-superusuários...')
        deleted_count = User.objects.filter(is_superuser=False).delete()[0]
        self.stdout.write(self.style.SUCCESS(f'✅ {deleted_count} usuário(s) deletado(s)'))

        # Criar ou atualizar usuário gabi
        self.stdout.write('👤 Configurando usuário "gabi"...')
        gabi, created = User.objects.get_or_create(username='gabi')
        gabi.set_password('borlaria')
        gabi.is_active = True
        gabi.is_staff = False
        gabi.is_superuser = False
        gabi.save()
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Usuário "gabi" criado'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Senha do usuário "gabi" atualizada'))

        # Criar ou atualizar usuário leo
        self.stdout.write('👤 Configurando usuário "leo"...')
        leo, created = User.objects.get_or_create(username='leo')
        leo.set_password('borlaria')
        leo.is_active = True
        leo.is_staff = False
        leo.is_superuser = False
        leo.save()
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Usuário "leo" criado'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Senha do usuário "leo" atualizada'))

        # Verificar usuários criados
        total_users = User.objects.filter(is_superuser=False).count()
        self.stdout.write(self.style.SUCCESS(f'\n✅ Setup concluído!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total de usuários não-superusuários: {total_users}'))
        self.stdout.write(self.style.SUCCESS('\n👥 Usuários disponíveis:'))
        self.stdout.write(self.style.SUCCESS('  - gabi (senha: borlaria)'))
        self.stdout.write(self.style.SUCCESS('  - leo (senha: borlaria)'))
        
        # Verificar se os usuários podem fazer login
        from django.contrib.auth import authenticate
        gabi_auth = authenticate(username='gabi', password='borlaria')
        leo_auth = authenticate(username='leo', password='borlaria')
        
        if gabi_auth and leo_auth:
            self.stdout.write(self.style.SUCCESS('\n✅ Verificação: Ambos os usuários podem fazer login!'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠️  Aviso: Algum usuário não pode fazer login. Verifique as senhas.'))
