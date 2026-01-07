from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message, UserPresence
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {username}! 💕')
            return redirect('chat')
        else:
            messages.error(request, 'Usuário ou senha incorretos 💔')
    return render(request, 'login.html')


# Chat
@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)
    selected_user = None
    messages_list = []

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

    if request.method == "POST":
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('message', '').strip()
        image = request.FILES.get('image')
        
        if receiver_id and (content or image):
            receiver = User.objects.get(id=receiver_id)
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content if content else None,
                image=image,
                timestamp=timezone.now()
            )
            
            # Notificar via WebSocket
            try:
                room_name = f"room_{min(request.user.id, int(receiver_id))}_{max(request.user.id, int(receiver_id))}"
                channel_layer = get_channel_layer()
                
                if channel_layer:
                    image_url = None
                    if message.image:
                        image_url = request.build_absolute_uri(message.image.url)
                    
                    async_to_sync(channel_layer.group_send)(
                        f'chat_{room_name}',
                        {
                            'type': 'chat_message',
                            'message': message.content or '',
                            'sender_id': request.user.id,
                            'sender_username': request.user.username,
                            'receiver_id': int(receiver_id),
                            'timestamp': message.timestamp.isoformat(),
                            'message_id': message.id,
                            'is_read': False,
                            'image_url': image_url,
                        }
                    )
            except Exception as e:
                # Se WebSocket falhar, continua normalmente (mensagem já foi salva)
                print(f"Erro ao notificar via WebSocket: {e}")

            if is_ajax:
                return JsonResponse({
                    'ok': True,
                    'message_id': message.id,
                    'timestamp': message.timestamp.isoformat(),
                    'image_url': image_url,
                    'message': message.content or '',
                })

            return redirect(f'/chat/?user={receiver_id}')

    user_id = request.GET.get('user')
    if user_id:
        selected_user = User.objects.get(id=user_id)
        messages_list = Message.objects.filter(
            sender__in=[request.user, selected_user],
            receiver__in=[request.user, selected_user]
        ).order_by('timestamp')
        
        # Marcar mensagens recebidas como lidas
        Message.objects.filter(
            receiver=request.user,
            sender=selected_user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

    # Presence data for user list + selected user
    user_ids = list(users.values_list('id', flat=True))
    presences = UserPresence.objects.filter(user_id__in=user_ids).select_related('user')
    presence_by_id = {p.user_id: p for p in presences}

    for u in users:
        p = presence_by_id.get(u.id)
        u.is_online = bool(p.is_online) if p else False
        u.last_seen = p.last_seen if p else None

    selected_presence = None
    if selected_user:
        selected_presence = UserPresence.objects.filter(user_id=selected_user.id).first()

    return render(request, 'chat.html', {
        'users': users,
        'selected_user': selected_user,
        'messages': messages_list,
        'selected_presence': selected_presence,
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Até logo, meu coração 💔")
    return redirect('login')
