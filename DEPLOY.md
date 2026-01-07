# 🚀 Guia de Deploy - Chatamor

O GitHub Pages **não suporta Django**. Você precisa usar um serviço que execute aplicações Python.

## 📋 Opções de Hospedagem Gratuita

### 1. **Railway** (Recomendado - Mais Fácil) ⭐

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório
6. Railway detectará automaticamente o Django
7. Adicione as variáveis de ambiente:
   - `SECRET_KEY` - Gere uma chave secreta
   - `DEBUG=False`
   - `ALLOWED_HOSTS=seu-app.railway.app`
   - `REDIS_URL` - Railway criará automaticamente um Redis
   - `DATABASE_URL` - Railway criará automaticamente um PostgreSQL

**Vantagens:**
- ✅ Grátis (com limites generosos)
- ✅ Setup automático
- ✅ Suporta PostgreSQL e Redis
- ✅ Deploy automático do GitHub

---

### 2. **Render** (Alternativa Gratuita)

1. Acesse [render.com](https://render.com)
2. Faça login com GitHub
3. Clique em "New +" → "Web Service"
4. Conecte seu repositório GitHub
5. Configure:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `daphne -b 0.0.0.0 -p $PORT base.asgi:application`
6. Adicione um **PostgreSQL** (New + → PostgreSQL)
7. Adicione um **Redis** (New + → Redis)
8. Configure as variáveis de ambiente:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=seu-app.onrender.com`
   - `DATABASE_URL` (copie da conexão do PostgreSQL)
   - `REDIS_URL` (copie da conexão do Redis)

**Vantagens:**
- ✅ Plano gratuito disponível
- ✅ Fácil de configurar
- ⚠️ Pode "dormir" após 15 minutos de inatividade (gratuito)

---

### 3. **PythonAnywhere** (Alternativa)

1. Acesse [pythonanywhere.com](https://www.pythonanywhere.com)
2. Crie uma conta gratuita
3. Configure manualmente via console

---

## 🔧 Variáveis de Ambiente Necessárias

Crie um arquivo `.env` ou configure no painel do serviço:

```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,seu-app.railway.app
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

**Para gerar SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📝 Passos Após Deploy

1. Execute as migrações (geralmente automático):
   ```bash
   python manage.py migrate
   ```

2. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

3. Configure usuários iniciais (se necessário):
   ```bash
   python manage.py setup_users
   ```

---

## 🌐 Após o Deploy

Seu app estará disponível em:
- **Railway:** `https://seu-app.railway.app`
- **Render:** `https://seu-app.onrender.com`

Acesse a URL e você verá a página de login do seu chat! 💕

---

## ⚠️ Importante

- O GitHub Pages **NÃO** pode hospedar Django
- Você precisa de um serviço que execute Python
- Railway e Render são as opções mais fáceis e gratuitas
- O `index.html` que estava na raiz não é necessário - seu Django já tem as rotas configuradas

---

## 🆘 Precisa de Ajuda?

Se tiver problemas no deploy, verifique:
1. ✅ Todas as variáveis de ambiente estão configuradas
2. ✅ O banco de dados está conectado
3. ✅ O Redis está configurado
4. ✅ `ALLOWED_HOSTS` inclui o domínio do serviço
