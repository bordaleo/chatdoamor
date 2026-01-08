# 🚀 Como Atualizar o Deploy (Sem Acesso ao Shell)

Como você está usando **Render** e não tem acesso ao shell, você precisa fazer **commit e push** das mudanças para o GitHub. O Render fará o deploy automaticamente!

## 📝 Passos para Atualizar

### 1. Adicionar as mudanças ao Git

No terminal (PowerShell ou Git Bash), execute:

```bash
git add chat/templates/chat.html chat/views.py chat/consumers.py
```

### 2. Fazer commit das mudanças

```bash
git commit -m "Corrigir: mensagens em tempo real, status online e visto por último"
```

### 3. Enviar para o GitHub

```bash
git push origin main
```

### 4. Aguardar o Deploy Automático

- O Render detectará automaticamente o push
- Irá fazer o build e deploy das mudanças
- Você pode acompanhar o progresso no painel do Render

## ⏱️ Tempo de Deploy

- Build: ~2-5 minutos
- Deploy: automático após o build

## ✅ Verificar se Funcionou

Após o deploy:

1. Acesse seu site no Render
2. Abra o console do navegador (F12)
3. Verifique se há erros
4. Teste:
   - Enviar mensagens (devem aparecer sem atualizar)
   - Status online (deve aparecer quando ambos estão conectados)
   - "Visto por último" (deve aparecer quando offline)

## 🆘 Se Algo Der Errado

1. Verifique os **logs** no painel do Render
2. Verifique se o **build** foi bem-sucedido
3. Se necessário, faça um **Manual Deploy** no painel do Render

## 📋 Arquivos Modificados

Os seguintes arquivos foram atualizados:

- ✅ `chat/templates/chat.html` - Removido polling de recarregamento, melhorias em tempo real
- ✅ `chat/views.py` - Notificação via WebSocket quando mensagens são marcadas como lidas
- ✅ `chat/consumers.py` - Marca mensagens como lidas automaticamente ao receber via WebSocket
- ✅ `render.yaml` - Atualizado domínios permitidos

## 🎯 Funcionalidades Implementadas

✅ **Mensagens em Tempo Real**
- Mensagens aparecem instantaneamente sem atualizar a página
- Funciona tanto para texto quanto para imagens

✅ **Status de Visualizado**
- Status de visualização atualiza em tempo real via WebSocket
- Marcação automática quando mensagem é recebida
- Atualização imediata quando outra pessoa visualiza

✅ **Status Online/Offline**
- Indicador online aparece em tempo real quando usuário conecta
- Status offline atualiza quando usuário desconecta
- "Visto por último" atualiza automaticamente

---

**Dica:** Se você quiser ver todas as mudanças antes de fazer commit:

```bash
git status
git diff chat/templates/chat.html
```
