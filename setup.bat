@echo off
REM Script de configuração inicial do projeto (Windows)

echo 🚀 Configurando Chatamor...

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo 🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📥 Instalando dependências...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Criar arquivo .env se não existir
if not exist ".env" (
    echo 📝 Criando arquivo .env...
    (
        echo SECRET_KEY=django-insecure-temp-key-change-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo REDIS_URL=redis://localhost:6379/0
        echo DATABASE_URL=sqlite:///db.sqlite3
    ) > .env
    echo ✅ Arquivo .env criado!
)

REM Executar migrações
echo 🗄️  Executando migrações...
python manage.py makemigrations
python manage.py migrate

REM Coletar arquivos estáticos
echo 📦 Coletando arquivos estáticos...
python manage.py collectstatic --noinput

echo ✅ Configuração concluída!
echo.
echo Para iniciar o servidor:
echo   python manage.py runserver
echo.
echo Não esqueça de iniciar o Redis!

pause
