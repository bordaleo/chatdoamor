# 🚀 Guia Rápido de Início

## Instalação Rápida

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Redis

**Windows:**
- Baixe o Redis do [redis.io](https://redis.io/download)
- Ou use WSL: `wsl sudo apt-get install redis-server`

**Linux/Mac:**
```bash
sudo apt-get install redis-server
# ou
brew install redis
```

Inicie o Redis:
```bash
redis-server
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

### 4. Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar Superusuário (Opcional)

```bash
python manage.py createsuperuser
```

### 6. Iniciar o Servidor

```bash
python manage.py runserver
```

Ou usando Daphne (recomendado para WebSockets):

```bash
daphne -b 0.0.0.0 -p 8000 base.asgi:application
```

## 🐳 Usando Docker

```bash
# Construir e iniciar
docker-compose up --build

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser
```

## 📝 Notas Importantes

1. **Redis é obrigatório** para o funcionamento dos WebSockets
2. O servidor deve ser iniciado com **Daphne** (não `runserver`) para WebSockets funcionarem em produção
3. Para desenvolvimento, `runserver` funciona, mas Daphne é recomendado

## 🔧 Solução de Problemas

### WebSocket não conecta
- Verifique se o Redis está rodando: `redis-cli ping` (deve retornar PONG)
- Certifique-se de usar Daphne: `daphne base.asgi:application`

### Erro de migração
- Execute: `python manage.py makemigrations chat`
- Depois: `python manage.py migrate`

### Erro de importação
- Ative o ambiente virtual: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
- Reinstale as dependências: `pip install -r requirements.txt`
