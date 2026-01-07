#!/bin/bash

# Script de configuração inicial do projeto

echo "🚀 Configurando Chatamor..."

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
fi

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo .env..."
    cat > .env << EOF
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///db.sqlite3
EOF
    echo "✅ Arquivo .env criado!"
fi

# Executar migrações
echo "🗄️  Executando migrações..."
python manage.py makemigrations
python manage.py migrate

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Configuração concluída!"
echo ""
echo "Para iniciar o servidor:"
echo "  python manage.py runserver"
echo ""
echo "Não esqueça de iniciar o Redis:"
echo "  redis-server"
