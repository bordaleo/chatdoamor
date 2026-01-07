#!/usr/bin/env python
"""
Script de inicialização robusto para produção (Render.com)
Verifica conexão do banco e executa migrações antes de iniciar o servidor
"""
import os
import sys
import time

# IMPORTANTE: Esta mensagem confirma que o script está sendo executado
print("=" * 60)
print("✅ ENTRYPOINT.PY ESTÁ SENDO EXECUTADO!")
print("=" * 60)
print(f"Python: {sys.executable}")
print(f"Versão: {sys.version}")
print(f"Diretório de trabalho: {os.getcwd()}")
print("=" * 60)

import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
try:
    django.setup()
    print("✅ Django configurado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao configurar Django: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

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
    
    # Fechar qualquer conexão existente
    try:
        connection.close()
    except:
        pass
    
    try:
        # Executar migrações com verbosidade máxima
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migrações aplicadas com sucesso!")
        
        # Verificar se auth_user existe
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'auth_user'")
                exists = cursor.fetchone()[0] > 0
                if exists:
                    print("✅ Tabela auth_user confirmada no banco de dados!")
                else:
                    print("⚠️  AVISO: Tabela auth_user não encontrada após migração!")
                    return False
        except Exception as e:
            print(f"⚠️  Não foi possível verificar tabela auth_user: {e}")
            # Continuar mesmo assim, pois pode ser um problema de permissão
            
        return True
    except (CommandError, Exception) as e:
        print(f"❌ Erro ao executar migrações: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        import traceback
        print(f"   Traceback completo:")
        traceback.print_exc()
        print("🔄 Tentando novamente em 5 segundos...")
        time.sleep(5)
        
        # Fechar conexão novamente
        try:
            connection.close()
        except:
            pass
        
        try:
            call_command('migrate', verbosity=2, interactive=False)
            print("✅ Migrações aplicadas com sucesso na segunda tentativa!")
            
            # Verificar novamente
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'auth_user'")
                    exists = cursor.fetchone()[0] > 0
                    if exists:
                        print("✅ Tabela auth_user confirmada no banco de dados!")
                    else:
                        print("⚠️  AVISO: Tabela auth_user não encontrada após migração!")
                        return False
            except Exception as e:
                print(f"⚠️  Não foi possível verificar tabela auth_user: {e}")
                
            return True
        except (CommandError, Exception) as e2:
            print(f"❌ Erro crítico: Não foi possível executar migrações!")
            print(f"   Erro: {e2}")
            print(f"   Tipo do erro: {type(e2).__name__}")
            import traceback
            traceback.print_exc()
            # Tentar mostrar mais informações sobre o banco
            try:
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
    print("=" * 60)
    print("🚀 Iniciando Chatamor - Script de Inicialização")
    print("=" * 60)
    print(f"📋 DATABASE_URL configurada: {'Sim' if os.environ.get('DATABASE_URL') else 'Não'}")
    if os.environ.get('DATABASE_URL'):
        # Mostrar apenas o início da URL (sem senha)
        db_url = os.environ.get('DATABASE_URL', '')
        if '@' in db_url:
            parts = db_url.split('@')
            if len(parts) > 0:
                print(f"   URL: {parts[0].split('://')[0]}://***@{parts[1] if len(parts) > 1 else ''}")
    
    # Verificar conexão do banco
    print("\n" + "=" * 60)
    print("PASSO 1: Verificando conexão com banco de dados")
    print("=" * 60)
    if not wait_for_db():
        print("⚠️  Aviso: Não foi possível verificar conexão, mas continuando...")
    
    # Executar migrações
    print("\n" + "=" * 60)
    print("PASSO 2: Executando migrações do banco de dados")
    print("=" * 60)
    if not run_migrations():
        print("\n" + "=" * 60)
        print("❌ ERRO CRÍTICO: Não foi possível executar migrações!")
        print("=" * 60)
        print("\n📋 Informações de diagnóstico:")
        print(f"   DATABASE_URL presente: {'Sim' if os.environ.get('DATABASE_URL') else 'Não'}")
        try:
            from django.conf import settings
            db_engine = settings.DATABASES['default'].get('ENGINE', 'N/A')
            db_name = settings.DATABASES['default'].get('NAME', 'N/A')
            db_host = settings.DATABASES['default'].get('HOST', 'N/A')
            print(f"   Engine do banco: {db_engine}")
            print(f"   Nome do banco: {db_name}")
            print(f"   Host do banco: {db_host}")
        except Exception as e:
            print(f"   Erro ao obter configuração: {e}")
        show_migrations_status()
        print("\n" + "=" * 60)
        print("❌ O servidor NÃO será iniciado devido ao erro acima!")
        print("=" * 60)
        sys.exit(1)
    
    # Mostrar status das migrações
    print("\n" + "=" * 60)
    print("PASSO 3: Verificando status das migrações")
    print("=" * 60)
    show_migrations_status()
    
    # Coletar arquivos estáticos (opcional)
    if os.environ.get('COLLECT_STATIC', '').lower() == 'true':
        print("\n" + "=" * 60)
        print("PASSO 4: Coletando arquivos estáticos")
        print("=" * 60)
        try:
            call_command('collectstatic', verbosity=1, interactive=False)
        except Exception as e:
            print(f"⚠️  Aviso: Erro ao coletar arquivos estáticos: {e}")
    
    # Iniciar servidor Daphne
    print("\n" + "=" * 60)
    print("PASSO 5: Iniciando servidor Daphne")
    print("=" * 60)
    port = os.environ.get('PORT', '8000')
    print(f"🚀 Iniciando servidor na porta {port}...")
    
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
