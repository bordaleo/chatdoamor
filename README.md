# 💞 Chatamor - Aplicativo de Chat Moderno

Um aplicativo de chat moderno e elegante construído com Django, Django Channels (WebSockets), Django REST Framework e muito amor! 💕

## ✨ Características

- 💬 **Chat em Tempo Real** - Usando WebSockets (Django Channels)
- 🎨 **Interface Moderna** - Design elegante e responsivo
- 🔐 **Autenticação Segura** - Sistema de login e registro
- 📱 **Responsivo** - Funciona perfeitamente em mobile e desktop
- 🚀 **API REST** - Django REST Framework para integração
- 📊 **Status de Leitura** - Veja quando suas mensagens foram lidas
- ⌨️ **Indicador de Digitação** - Saiba quando alguém está digitando
- 🐳 **Docker** - Containerização completa
- 🔒 **Segurança** - Configurações de segurança modernas

## 🛠️ Tecnologias

- **Backend:**
  - Django 5.2.7
  - Django Channels (WebSockets)
  - Django REST Framework
  - Redis (para Channel Layers)
  - PostgreSQL (opcional, SQLite por padrão)

- **Frontend:**
  - HTML5, CSS3, JavaScript (ES6+)
  - WebSockets API
  - Design responsivo e moderno

- **DevOps:**
  - Docker & Docker Compose
  - WhiteNoise (servir arquivos estáticos)

## 📦 Instalação

### Opção 1: Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd base
```

2. Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

3. Inicie os containers:
```bash
docker-compose up --build
```

4. Execute as migrações:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

5. Acesse `http://localhost:8000`

### Opção 2: Instalação Local

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd base
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o Redis (necessário para WebSockets):
   - **Windows:** Baixe e instale o Redis do [redis.io](https://redis.io/download)
   - **Linux/Mac:** `sudo apt-get install redis-server` ou `brew install redis`

5. Crie um arquivo `.env`:
```bash
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

6. Execute as migrações:
```bash
python manage.py migrate
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

8. Em outro terminal, inicie o Redis:
```bash
redis-server
```

9. Acesse `http://localhost:8000`

## 🚀 Uso

1. **Registre-se** ou **Faça login** na aplicação
2. **Selecione um usuário** da lista para começar a conversar
3. **Digite sua mensagem** e envie
4. As mensagens aparecem em **tempo real** usando WebSockets!

## 📡 API REST

A aplicação também expõe uma API REST completa:

### Endpoints Disponíveis

- `GET /api/users/` - Lista todos os usuários
- `GET /api/messages/` - Lista todas as mensagens do usuário autenticado
- `POST /api/messages/` - Cria uma nova mensagem
- `GET /api/messages/conversation/?user_id=<id>` - Obtém conversa com um usuário
- `GET /api/messages/unread_count/` - Conta mensagens não lidas
- `POST /api/messages/<id>/mark_as_read/` - Marca mensagem como lida
- `POST /api/auth/login/` - Autenticação via token

### Exemplo de Uso da API

```bash
# Obter token de autenticação
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'

# Listar mensagens
curl -H "Authorization: Token seu_token_aqui" \
  http://localhost:8000/api/messages/
```

## 🏗️ Estrutura do Projeto

```
base/
├── base/              # Configurações do Django
│   ├── settings.py   # Configurações modernas
│   ├── urls.py       # URLs principais
│   └── asgi.py       # Configuração ASGI para Channels
├── chat/             # App principal
│   ├── models.py     # Modelos (Message)
│   ├── views.py      # Views tradicionais
│   ├── api_views.py  # Views da API REST
│   ├── serializers.py # Serializers DRF
│   ├── consumers.py  # WebSocket consumers
│   ├── routing.py    # WebSocket routing
│   └── templates/    # Templates HTML
├── static/           # Arquivos estáticos
├── media/            # Arquivos de mídia
├── requirements.txt  # Dependências Python
├── Dockerfile        # Configuração Docker
└── docker-compose.yml # Orquestração Docker
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuração de Produção

Para produção, certifique-se de:

1. Definir `DEBUG=False`
2. Configurar `ALLOWED_HOSTS` corretamente
3. Usar um banco de dados PostgreSQL
4. Configurar SSL/HTTPS
5. Usar um servidor Redis em produção
6. Configurar WhiteNoise para servir arquivos estáticos

## 📝 Migrações

Após adicionar novos campos ao modelo `Message`, execute:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Testes

```bash
python manage.py test
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

## 💝 Feito com Amor

Desenvolvido com muito carinho e as melhores práticas modernas de desenvolvimento web.

---

**Desfrute do seu chat moderno! 💞**
