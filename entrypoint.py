#!/usr/bin/env python
"""
Script de inicialização robusto para produção (Render.com)
Verifica conexão do banco e executa migrações antes de iniciar o servidor
"""
import os
import sys
import time
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
from django.core.management.base import CommandError


def wait_for_db(max_attempts=30, delay=2):
    """Aguarda o banco de dados estar pronto para conexão"""
    print("⏳ Aguardando banco de dados estar pronto...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            connection.ensure_connection()
            print("✅ Banco de dados conectado!")
            return True
        except Exception as e:
            if attempt < max_attempts:
                print(f"⏳ Tentativa {attempt}/{max_attempts}: {e}")
                time.sleep(delay)
            else:
                print(f"❌ Erro: Não foi possível conectar ao banco de dados após {max_attempts} tentativas")
                print(f"   Último erro: {e}")
                return False
    
    return False


def run_migrations():
    """Executa as migrações do Django"""
    print("🗄️  Executando migrações do banco de dados...")
    
    try:
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Migrações aplicadas com sucesso!")
        return True
    except (CommandError, Exception) as e:
        print(f"❌ Erro ao executar migrações: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        print("🔄 Tentando novamente em 5 segundos...")
        time.sleep(5)
        
        try:
            call_command('migrate', verbosity=1, interactive=False)
            print("✅ Migrações aplicadas com sucesso na segunda tentativa!")
            return True
        except (CommandError, Exception) as e2:
            print(f"❌ Erro crítico: Não foi possível executar migrações!")
            print(f"   Erro: {e2}")
            print(f"   Tipo do erro: {type(e2).__name__}")
            # Tentar mostrar mais informações sobre o banco
            try:
                from django.db import connection
                db_info = connection.get_connection_params()
                print(f"   Configuração do banco: {db_info.get('database', 'N/A')}")
            except:
                pass
            return False


def show_migrations_status():
    """Mostra o status das migrações"""
    print("🔍 Verificando status das migrações...")
    try:
        call_command('showmigrations', verbosity=1)
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível verificar status: {e}")


def main():
    """Função principal"""
    print("🚀 Iniciando Chatamor...")
    print(f"📋 DATABASE_URL configurada: {'Sim' if os.environ.get('DATABASE_URL') else 'Não'}")
    
    # Verificar conexão do banco
    if not wait_for_db():
        print("⚠️  Aviso: Não foi possível verificar conexão, mas continuando...")
    
    # Executar migrações
    if not run_migrations():
        print("\n❌ ERRO CRÍTICO: Não foi possível executar migrações!")
        print("\n📋 Informações de diagnóstico:")
        print(f"   DATABASE_URL presente: {'Sim' if os.environ.get('DATABASE_URL') else 'Não'}")
        try:
            from django.conf import settings
            db_engine = settings.DATABASES['default'].get('ENGINE', 'N/A')
            print(f"   Engine do banco: {db_engine}")
        except Exception as e:
            print(f"   Erro ao obter configuração: {e}")
        show_migrations_status()
        sys.exit(1)
    
    # Mostrar status das migrações
    show_migrations_status()
    
    # Coletar arquivos estáticos (opcional)
    if os.environ.get('COLLECT_STATIC', '').lower() == 'true':
        print("📦 Coletando arquivos estáticos...")
        try:
            call_command('collectstatic', verbosity=1, interactive=False)
        except Exception as e:
            print(f"⚠️  Aviso: Erro ao coletar arquivos estáticos: {e}")
    
    # Iniciar servidor Daphne
    print("🚀 Iniciando servidor Daphne...")
    port = os.environ.get('PORT', '8000')
    
    try:
        # Executar Daphne
        os.execvp('daphne', [
            'daphne',
            '-b', '0.0.0.0',
            '-p', port,
            'base.asgi:application'
        ])
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
