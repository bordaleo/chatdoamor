# 🚨 AÇÃO IMEDIATA - Resolver Erro "auth_user"

## ⚡ O QUE FAZER AGORA (5 minutos)

### 1️⃣ Criar PostgreSQL no Render
```
Render Dashboard → "New +" → "PostgreSQL"
Name: chatamor-db
Database: chatamor  
User: chatamor
→ Criar
```

### 2️⃣ Copiar Internal Database URL
```
No banco criado → "Info" → Copiar "Internal Database URL"
(Formato: postgresql://chatamor:senha@dpg-xxx:5432/chatamor)
```

### 3️⃣ Adicionar DATABASE_URL no Web Service
```
Web Service → "Environment" → "Add Environment Variable"
Key: DATABASE_URL
Value: <cole-a-url-copiada>
→ Save
```

### 4️⃣ Criar Redis (se não existir)
```
"New +" → "Redis"
Name: chatamor-redis
→ Criar
→ Copiar Internal Redis URL
→ Web Service → Environment → Add REDIS_URL
```

### 5️⃣ Fazer Deploy
```
Web Service → "Manual Deploy" → "Clear build cache & deploy"
```

### 6️⃣ Verificar Logs
```
Web Service → "Logs"
Procurar por: "Running migrations..." e "OK"
```

---

## ❓ Se ainda não funcionar:

**Opção A:** Executar migrações manualmente
```
Web Service → "Shell" → "Connect"
python manage.py migrate
```

**Opção B:** Ver guia completo
```
Leia: PASSO_A_PASSO_RENDER.md
```

---

## ✅ Checklist Rápido

- [ ] PostgreSQL criado
- [ ] DATABASE_URL adicionada
- [ ] Redis criado e REDIS_URL adicionada
- [ ] Deploy executado
- [ ] Logs mostram "Running migrations... OK"

---

**Tempo estimado:** 5-10 minutos  
**Resultado:** Erro resolvido! 🎉
