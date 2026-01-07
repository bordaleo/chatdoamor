#!/bin/bash
# Script de inicialização para produção
# Executa migrações e inicia o servidor

set -e

echo "🚀 Iniciando Chatamor usando entrypoint.py..."
exec python entrypoint.py
