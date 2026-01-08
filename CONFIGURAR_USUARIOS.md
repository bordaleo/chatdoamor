# 👥 Configuração de Usuários

## 📋 Usuários do Sistema

O sistema possui apenas **2 usuários**:

- **Usuário:** `gabi` | **Senha:** `borlaria`
- **Usuário:** `leo` | **Senha:** `borlaria`

## 🚀 Como Configurar os Usuários

### Opção 1: Automático (Recomendado)

Os usuários são criados automaticamente quando o servidor inicia através do script `entrypoint.py`. Isso acontece após as migrações serem aplicadas.

### Opção 2: Manual via Shell do Render

Se os usuários não foram criados automaticamente, execute manualmente:

1. Acesse o painel do Render: https://dashboard.render.com
2. Vá em seu Web Service → **Shell** → **Connect**
3. Execute o comando:

```bash
python manage.py setup_users
```

Você verá:
```
✅ Mensagens deletadas
✅ X usuário(s) deletado(s)
✅ Usuário "gabi" criado
✅ Usuário "leo" criado
✅ Setup concluído!
```

### Opção 3: Local (Desenvolvimento)

Se estiver rodando localmente:

```bash
python manage.py setup_users
```

## 🔍 Verificar Usuários

Para verificar se os usuários foram criados corretamente:

```bash
python manage.py shell
```

Dentro do shell Python:

```python
from django.contrib.auth.models import User

# Listar todos os usuários
users = User.objects.all()
for user in users:
    print(f"Username: {user.username}, Ativo: {user.is_active}, Superuser: {user.is_superuser}")

# Verificar se gabi e leo existem
gabi = User.objects.filter(username='gabi').first()
leo = User.objects.filter(username='leo').first()

if gabi:
    print(f"✅ gabi existe e está {'ativo' if gabi.is_active else 'inativo'}")
if leo:
    print(f"✅ leo existe e está {'ativo' se leo.is_active else 'inativo'}")

# Testar autenticação
from django.contrib.auth import authenticate
gabi_auth = authenticate(username='gabi', password='borlaria')
leo_auth = authenticate(username='leo', password='borlaria')

print(f"gabi pode fazer login: {gabi_auth is not None}")
print(f"leo pode fazer login: {leo_auth is not None}")
```

## ⚠️ Importante

- O comando `setup_users` **deleta todos os usuários não-superusuários** antes de criar gabi e leo
- **Superusuários não são afetados** pelo comando
- As mensagens também são deletadas quando o comando é executado
- Os usuários são criados com `is_active=True` para permitir login

## 🆘 Problemas Comuns

### "Usuário ou senha incorretos"

1. Verifique se os usuários existem:
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   User.objects.filter(username__in=['gabi', 'leo']).values('username', 'is_active')
   ```

2. Reconfigure os usuários:
   ```bash
   python manage.py setup_users
   ```

3. Verifique se a senha está correta testando:
   ```python
   from django.contrib.auth import authenticate
   user = authenticate(username='gabi', password='borlaria')
   print(f"Autenticação: {user}")
   ```

### Usuários não aparecem no login

- Certifique-se de que `is_active=True` para ambos os usuários
- Execute `python manage.py setup_users` novamente

---

**Última atualização:** 2026-01-07
