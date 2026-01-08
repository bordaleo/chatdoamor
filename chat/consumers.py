import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, UserPresence
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')
        
        if message_type == 'message':
            message = text_data_json['message']
            sender_id = text_data_json['sender_id']
            receiver_id = text_data_json['receiver_id']
            
            # Save message to database
            saved_message = await self.save_message(sender_id, receiver_id, message)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'sender_username': await self.get_username(sender_id),
                    'receiver_id': receiver_id,
                    'timestamp': saved_message['timestamp'],
                    'message_id': saved_message['id'],
                }
            )
        elif message_type == 'typing':
            # Broadcast typing indicator
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': text_data_json['user_id'],
                    'username': await self.get_username(text_data_json['user_id']),
                    'is_typing': text_data_json['is_typing'],
                }
            )
        elif message_type == 'read_receipt':
            # Mark message as read
            message_id = text_data_json['message_id']
            read_at = await self.mark_message_as_read(message_id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_receipt',
                    'message_id': message_id,
                    'read_by': text_data_json['user_id'],
                    'read_at': read_at,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        message_data = {
            'type': 'message',
            'message': event.get('message', ''),
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'receiver_id': event['receiver_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
            'is_read': event.get('is_read', False),
        }
        
        if event.get('image_url'):
            message_data['image_url'] = event['image_url']
        
        await self.send(text_data=json.dumps(message_data))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_typing': event['is_typing'],
        }))

    async def read_receipt(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'message_id': event['message_id'],
            'read_by': event['read_by'],
            'read_at': event.get('read_at'),
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            timestamp=timezone.now()
        )
        return {
            'id': message.id,
            'timestamp': message.timestamp.isoformat(),
        }

    @database_sync_to_async
    def get_username(self, user_id):
        return User.objects.get(id=user_id).username

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            message.mark_as_read()
            return message.read_at.isoformat() if message.read_at else None
        except Message.DoesNotExist:
            return None


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.user_id = user.id
        self.group_name = 'presence'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Mark online and broadcast
        presence = await self.set_online(self.user_id)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'presence_update',
                'user_id': self.user_id,
                'is_online': True,
                'last_seen': presence.get('last_seen'),
            }
        )

        # Send snapshot to this connection
        snapshot = await self.get_presence_snapshot(exclude_user_id=self.user_id)
        await self.send(text_data=json.dumps({
            'type': 'presence_snapshot',
            'users': snapshot,
        }))

    async def disconnect(self, close_code):
        user_id = getattr(self, 'user_id', None)
        if user_id:
            presence = await self.set_offline(user_id)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'presence_update',
                    'user_id': user_id,
                    'is_online': False,
                    'last_seen': presence.get('last_seen'),
                }
            )

        await self.channel_layer.group_discard(getattr(self, 'group_name', 'presence'), self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get('type') == 'ping':
                # Responder ao ping para manter conexão ativa
                await self.send(text_data=json.dumps({'type': 'pong'}))
        except:
            pass

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'presence_update',
            'user_id': event['user_id'],
            'is_online': event['is_online'],
            'last_seen': event.get('last_seen'),
        }))

    @database_sync_to_async
    def set_online(self, user_id):
        user = User.objects.get(id=user_id)
        presence, _ = UserPresence.objects.get_or_create(user=user)
        if presence.last_seen is None:
            presence.last_seen = timezone.now()
        if not presence.is_online:
            presence.is_online = True
        presence.save(update_fields=['is_online', 'last_seen', 'updated_at'])
        return {
            'last_seen': presence.last_seen.isoformat() if presence.last_seen else None,
        }

    @database_sync_to_async
    def set_offline(self, user_id):
        user = User.objects.get(id=user_id)
        presence, _ = UserPresence.objects.get_or_create(user=user)
        presence.is_online = False
        presence.last_seen = timezone.now()
        presence.save(update_fields=['is_online', 'last_seen', 'updated_at'])
        return {
            'last_seen': presence.last_seen.isoformat() if presence.last_seen else None,
        }

    @database_sync_to_async
    def get_presence_snapshot(self, exclude_user_id=None):
        qs = UserPresence.objects.select_related('user').all()
        if exclude_user_id:
            qs = qs.exclude(user_id=exclude_user_id)
        return [
            {
                'user_id': p.user_id,
                'is_online': p.is_online,
                'last_seen': p.last_seen.isoformat() if p.last_seen else None,
            }
            for p in qs
        ]
