# 🔧 Configuração Manual no Render

Se o `render.yaml` não estiver funcionando automaticamente, siga estes passos:

## 1. Criar Banco de Dados PostgreSQL

1. No painel do Render, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `chatamor-db`
   - **Database:** `chatamor`
   - **User:** `chatamor`
   - Escolha o plano (Free tier funciona)
3. Anote a **Internal Database URL** (será algo como `postgresql://chatamor:senha@dpg-xxx:5432/chatamor`)

## 2. Criar Redis

1. No painel do Render, clique em **"New +"** → **"Redis"**
2. Configure:
   - **Name:** `chatamor-redis`
   - Escolha o plano (Free tier funciona)
3. Anote a **Internal Redis URL** (será algo como `redis://red-xxx:6379`)

## 3. Configurar Web Service

1. No painel do Render, vá em seu **Web Service**
2. Clique em **"Environment"**
3. Adicione/atualize estas variáveis de ambiente:

### Variáveis Obrigatórias:

```
SECRET_KEY=<gere-uma-chave-secreta-aqui>
DEBUG=False
ALLOWED_HOSTS=chatdoamor.onrender.com
CSRF_TRUSTED_ORIGINS=https://chatdoamor.onrender.com,http://chatdoamor.onrender.com
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Variáveis do Banco de Dados:

```
DATABASE_URL=<cole-a-internal-database-url-do-postgresql>
REDIS_URL=<cole-a-internal-redis-url>
```

**⚠️ IMPORTANTE:** Use a **Internal Database URL** e **Internal Redis URL**, não as URLs externas!

## 4. Configurar Build e Start Commands

No seu Web Service, vá em **"Settings"** e configure:

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
python manage.py migrate --noinput && daphne -b 0.0.0.0 -p $PORT base.asgi:application
```

## 5. Gerar SECRET_KEY

Para gerar uma SECRET_KEY segura, execute localmente:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Ou use este comando Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 6. Verificar Logs

Após o deploy, verifique os logs para garantir que:
- ✅ As migrações foram executadas
- ✅ O banco de dados está conectado (não SQLite)
- ✅ O servidor iniciou corretamente

## 🆘 Problemas Comuns

### "no such table: auth_user"
- **Causa:** Migrações não foram executadas
- **Solução:** Verifique se o `startCommand` inclui `python manage.py migrate --noinput`

### "OperationalError" ou "connection refused"
- **Causa:** DATABASE_URL ou REDIS_URL incorretos
- **Solução:** Use as **Internal URLs** do Render, não as externas

### Ainda usando SQLite
- **Causa:** DATABASE_URL não está configurado
- **Solução:** Verifique se a variável `DATABASE_URL` está configurada no painel do Render

## ✅ Checklist Final

- [ ] PostgreSQL criado e Internal Database URL copiada
- [ ] Redis criado e Internal Redis URL copiada
- [ ] Todas as variáveis de ambiente configuradas
- [ ] Build Command configurado
- [ ] Start Command inclui `migrate --noinput`
- [ ] SECRET_KEY gerada e configurada
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado com seu domínio
- [ ] CSRF_TRUSTED_ORIGINS configurado

Após configurar tudo, faça um **Manual Deploy** no Render para aplicar as mudanças.
