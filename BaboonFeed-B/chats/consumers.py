import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from chats.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.isPrivate = self.scope['path'].find('private') != -1
        self.room_name = (
            self.scope['url_route']['kwargs']['room_name']
            if not self.isPrivate
            else f'user_{self.scope["url_route"]["kwargs"]["room_name"]}'
        )
        self.room_group_name = f'chat_{self.room_name}'

        # Realizar la autenticación con el token recibido
        self.token = None
        self.user = AnonymousUser()

        # Únete al grupo de WebSocket
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de WebSocket
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)

        # Esperar el primer mensaje para autenticar
        if message.get('type') == 'auth' and message.get('token'):
            access_token = AccessToken(message['token'])
            self.user = await self.get_user(id=access_token['user_id'])
            return

        # Si no se autenticó correctamente, cerrar la conexión
        if self.user == AnonymousUser():
            await self.close()

        if self.isPrivate:
            receiver = await self.get_user(username=message['receiver'])
            group = None
        else:
            receiver = None
            group = await self.get_user(id=self.room_name)

        await sync_to_async(Message.objects.create)(
            content=message['content'], author=self.user, receiver=receiver, group=group
        )
        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )

    async def chat_message(self, event):
        message = event['message']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({'message': message}))
        if group := message.group:
            for member in group.members:
                notify_user(member.username, message.content, group.name)
        else:
            notify_user(message.receiver, message.content, message.author.username)

    @database_sync_to_async
    def get_user(self, username=None, id=None):
        try:
            if id:
                return get_user_model().objects.get(id=id)
            return get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None

    def notify_user(user_id, message, sender):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user_id}',
            {'type': 'send_notification', 'message': message, 'sender': sender},
        )


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f'notifications_{self.user.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.user:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'type': event.get('type'),
                    'message': event.get('message'),
                    'sender': event.get('sender'),
                }
            )
        )
