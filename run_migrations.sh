#!/bin/bash
# Script simples para executar migrações
# Use este script se entrypoint.py não funcionar

set -e

echo "🗄️  Executando migrações..."
python manage.py migrate --noinput

echo "✅ Migrações concluídas!"
