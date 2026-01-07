# 📋 Instruções de Configuração

## ✅ Mudanças Implementadas

1. ✅ **Usuários limitados**: Apenas "gabi" e "leo" com senha "borlaria"
2. ✅ **Cores personalizadas**: Rosa para gabi, azul para leo
3. ✅ **Registro removido**: Não é mais possível criar novos usuários
4. ✅ **Upload de fotos**: Suporte completo para envio de imagens
5. ✅ **Visualização de mensagens**: Sistema como WhatsApp (✓ e ✓✓)
6. ✅ **Envio offline**: Mensagens são salvas e enviadas quando voltar online
7. ✅ **Horário de Brasília**: Timezone configurado para America/Sao_Paulo

## 🚀 Passos para Configurar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Usuários

Execute o comando para limpar e criar apenas gabi e leo:

```bash
python manage.py setup_users
```

Isso irá:
- Deletar todas as mensagens antigas
- Deletar todos os usuários (exceto superusuários)
- Criar usuário "gabi" com senha "borlaria"
- Criar usuário "leo" com senha "borlaria"

### 3. Criar Migrações e Aplicar

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Iniciar Redis (Obrigatório para WebSockets)

**Windows:**
- Baixe e instale Redis do site oficial
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

### 5. Iniciar o Servidor

```bash
python manage.py runserver
```

Ou com Daphne (recomendado para WebSockets):
```bash
daphne -b 0.0.0.0 -p 8000 base.asgi:application
```

## 📝 Notas Importantes

- **Redis é obrigatório** para WebSockets funcionarem
- O timezone já está configurado para Brasília (America/Sao_Paulo)
- As cores mudam automaticamente baseado no usuário logado
- Mensagens offline são salvas e enviadas quando a conexão voltar
- Visualizações (✓✓) aparecem quando a mensagem é lida

## 🎨 Cores

- **Gabi**: Tema rosa (gradiente rosa/pink)
- **Leo**: Tema azul (gradiente azul)

## 📸 Upload de Imagens

- Clique no botão 📷 para selecionar uma imagem
- Você pode enviar apenas imagem, apenas texto, ou ambos
- As imagens são exibidas no chat e podem ser clicadas para ampliar

## 🔍 Visualização de Mensagens

- **✓** (cinza): Mensagem enviada, não visualizada
- **✓✓** (verde): Mensagem visualizada pelo destinatário

As mensagens são marcadas como lidas automaticamente quando o destinatário abre a conversa.
