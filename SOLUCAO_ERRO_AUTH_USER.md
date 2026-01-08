# 🔧 Solução Passo a Passo: Erro "no such table: auth_user"

## 📋 Entendendo o Problema

O erro `OperationalError: no such table: auth_user` acontece porque:
- As migrações do Django não foram executadas no banco de dados
- As tabelas do sistema de autenticação do Django (`auth_user`, etc.) não foram criadas
- Isso é comum após o primeiro deploy ou quando o banco de dados é recriado

---

## ✅ Solução Rápida (Render.com)

### **Passo 1: Verificar o Start Command no Render**

1. Acesse o painel do Render: https://dashboard.render.com
2. Clique no seu **Web Service** (chatamor)
3. Vá em **"Settings"** → **"Build & Deploy"**
4. Encontre o campo **"Start Command"**

**⚠️ Se NÃO encontrar o Start Command:**
- O Render está usando o `Procfile` automaticamente
- O `Procfile` já foi corrigido com o comando de migrate
- Você só precisa fazer commit e push, OU configurar manualmente (veja guia completo)

**Se encontrar o campo, verifique se está assim:**

```bash
python manage.py migrate --noinput && daphne -b 0.0.0.0 -p $PORT base.asgi:application
```

**⚠️ Se não estiver assim, copie e cole exatamente o comando acima!**

---

### **Passo 2: Criar PostgreSQL e Configurar DATABASE_URL**

⚠️ **IMPORTANTE:** Se você não encontrou o Start Command, o `DATABASE_URL` não existe, siga o guia completo detalhado:

📖 **Guia Completo:** Veja `PASSO_A_PASSO_RENDER.md` para instruções passo a passo com screenshots mentais.

**Resumo rápido:**

1. **Criar PostgreSQL:**
   - Render → "New +" → "PostgreSQL"
   - Name: `chatamor-db`, Database: `chatamor`, User: `chatamor`
   
2. **Copiar Internal Database URL:**
   - No banco criado, vá em "Info" ou "Connections"
   - Copie a **Internal Database URL** (não a externa!)
   - Formato: `postgresql://chatamor:senha@dpg-xxx:5432/chatamor`

3. **Adicionar no Web Service:**
   - Web Service → "Environment" → "Add Environment Variable"
   - Key: `DATABASE_URL`
   - Value: `<cole-a-url-copiada>`
   - Save Changes

---

### **Passo 3: Fazer Manual Deploy**

1. No painel do Render, vá em **"Manual Deploy"**
2. Clique em **"Deploy latest commit"** ou **"Clear build cache & deploy"**
3. Aguarde o deploy terminar
4. Verifique os **Logs** para garantir que apareceu:
   ```
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, sessions, chat
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     ...
   ```

---

## 🔍 Verificação após o Deploy

Após o deploy, verifique nos **Logs** se:

1. ✅ **Migrações foram executadas:**
   ```
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, sessions, chat
   Running migrations:
     Applying auth.0001_initial... OK
   ```

2. ✅ **Não está usando SQLite:**
   - Se você ver algo como `db.sqlite3`, está errado
   - Deve mostrar conexão com PostgreSQL

3. ✅ **Servidor iniciou:**
   ```
   Starting server at tcp:port:0.0.0.0:10000
   Application startup complete.
   ```

---

## 🆘 Se Ainda Não Funcionar

### Opção 1: Usar o Shell do Render (Recomendado)

1. No painel do Render, vá em **"Shell"** (ao lado de Logs)
2. Clique em **"Connect"**
3. Execute manualmente:

```bash
python manage.py migrate
python manage.py migrate --run-syncdb
```

4. Verifique se deu certo:
```bash
python manage.py showmigrations
```

Todas devem aparecer com `[X]` (aplicadas).

---

### Opção 2: Verificar se o Build Command está correto

1. No Render, vá em **Settings** → **Build & Deploy**
2. O **Build Command** deve ser:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

3. O **Start Command** deve ser:
```bash
python manage.py migrate --noinput && daphne -b 0.0.0.0 -p $PORT base.asgi:application
```

---

### Opção 3: Forçar recriação do banco (⚠️ Apaga todos os dados!)

**⚠️ ATENÇÃO: Isso vai apagar todos os dados do banco!**

1. No Shell do Render, execute:
```bash
python manage.py flush --noinput
python manage.py migrate
```

2. Se necessário, recrie os usuários:
```bash
python manage.py setup_users
```

---

## 📝 Checklist de Verificação

Antes de considerar resolvido, verifique:

- [ ] `DATABASE_URL` está configurada no Render (não vazia)
- [ ] O banco é PostgreSQL (não SQLite)
- [ ] Start Command inclui `python manage.py migrate --noinput`
- [ ] Build Command está correto
- [ ] Manual Deploy foi executado
- [ ] Logs mostram "Running migrations" com sucesso
- [ ] Acessar http://chatdoamor.onrender.com não mostra mais o erro

---

## 🎯 Resumo Rápido

**O problema:** Migrações não foram executadas no banco de dados.

**A solução:**
1. ✅ Verificar/corrigir o Start Command no Render
2. ✅ Garantir que DATABASE_URL está configurada
3. ✅ Fazer Manual Deploy
4. ✅ Verificar nos logs que migrações foram aplicadas

---

## 💡 Dica Final

Se você atualizou o `Procfile` localmente (já foi corrigido para incluir migrate), faça commit e push:

```bash
git add Procfile
git commit -m "Fix: Add migrate to Procfile startup"
git push
```

O Render vai fazer deploy automático e aplicar as migrações! 🚀
