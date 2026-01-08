#!/bin/bash
# Script de inicialização robusto para produção (Render.com)
# Verifica conexão do banco e executa migrações antes de iniciar o servidor

set -e  # Para na primeira falha

echo "🚀 Iniciando Chatamor..."

# Função para verificar conexão do banco de dados
wait_for_db() {
    echo "⏳ Aguardando banco de dados estar pronto..."
    max_attempts=30
    attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print('✅ Banco de dados conectado!')
    exit(0)
except Exception as e:
    print(f'⏳ Tentativa {${attempt} + 1}/${max_attempts}: {e}')
    exit(1)
" 2>/dev/null; then
            echo "✅ Banco de dados está pronto!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo "⏳ Tentativa $attempt/$max_attempts: Aguardando banco de dados..."
        sleep 2
    done
    
    echo "❌ Erro: Não foi possível conectar ao banco de dados após $max_attempts tentativas"
    return 1
}

# Verificar conexão do banco
wait_for_db || {
    echo "⚠️  Aviso: Não foi possível verificar conexão, mas continuando..."
}

# Executar migrações com tratamento de erro
echo "🗄️  Executando migrações do banco de dados..."
if python manage.py migrate --noinput; then
    echo "✅ Migrações aplicadas com sucesso!"
else
    echo "❌ Erro ao executar migrações!"
    echo "🔄 Tentando novamente..."
    sleep 5
    if ! python manage.py migrate --noinput; then
        echo "❌ Erro crítico: Não foi possível executar migrações!"
        echo "📋 Verificando status das migrações..."
        python manage.py showmigrations || true
        exit 1
    fi
fi

# Verificar se as migrações foram aplicadas corretamente
echo "🔍 Verificando migrações aplicadas..."
python manage.py showmigrations | grep -E "\[X\]|\[ \]" || true

# Coletar arquivos estáticos (se necessário)
if [ -n "$COLLECT_STATIC" ] && [ "$COLLECT_STATIC" = "true" ]; then
    echo "📦 Coletando arquivos estáticos..."
    python manage.py collectstatic --noinput || echo "⚠️  Aviso: Erro ao coletar arquivos estáticos"
fi

# Iniciar servidor
echo "🚀 Iniciando servidor Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-8000} base.asgi:application
