import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from files.models import File
from groups.models import GroupChat
from rest_framework_simplejwt.tokens import AccessToken

from chats.models import Chat, Message


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_user = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_user_{self.room_user}'

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

        receiver = await self.get_user(username=message['receiver'])
        chat = await self.get_or_create_private_chat(self.user, receiver)

        file = await get_file(message['file']['id']) if message.get('file') else None

        new_message = await sync_to_async(Message.objects.create)(
            content=message['content'], author=self.user, receiver=receiver, chat=chat, file=file
        )

        chat.last_message = new_message
        await sync_to_async(chat.save)()

        serialzed_message = serialize_message(new_message, scope=self.scope)

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': serialzed_message},
        )

        await self.channel_layer.group_send(
            f'chat_user_{message["receiver"]}',
            {'type': 'chat_message', 'message': serialzed_message},
        )

    @sync_to_async
    def get_or_create_private_chat(self, user1, user2):
        # Buscar un chat privado con exactamente esos 2 usuarios
        chat = Chat.objects.filter(members__username__in=[user1, user2])

        if chat.exists():
            return chat.first()

        # Crear el chat si no existe
        chat = Chat.objects.create()
        chat.members.add(user1, user2)
        return chat

    async def chat_message(self, event):
        message = event['message']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def get_user(self, username=None, id=None):
        try:
            if id:
                return get_user_model().objects.get(id=id)
            return get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_group_{self.group_id}'

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

        group_chat = await self.get_group_chat(id=self.group_id)
        if group_chat is None:
            return

        file = await get_file(message['file']['id']) if message.get('file') else None

        new_message = await sync_to_async(Message.objects.create)(
            content=message['content'], author=self.user, group=group_chat, file=file
        )

        group_chat.last_message = new_message
        await sync_to_async(group_chat.save)()

        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat_message', 'message': serialize_message(new_message, scope=self.scope)}
        )

    async def chat_message(self, event):
        message = event['message']
        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def get_user(self, username=None, id=None):
        try:
            if id:
                return get_user_model().objects.get(id=id)
            return get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None

    @database_sync_to_async
    def get_group_chat(self, id):
        try:
            return GroupChat.objects.get(id=id)
        except GroupChat.DoesNotExist:
            return None


def serialize_message(message: Message, scope=None) -> dict:
    return {
        'id': message.id,
        'content': message.content,
        'created_at': message.created_at.isoformat(),
        'author': message.author.username,
        'receiver': message.receiver.username if message.receiver else None,
        'group': message.group.id if message.group else None,
        'chat': str(message.chat.id) if message.chat else None,
        'file': serialize_file(message.file)
    }


def serialize_file(file: File, scope=None) -> dict:
    if not file:
        return None

    if scope:
        scheme = 'https' if scope.get('scheme') == 'https' else 'http'
        host_header = dict(scope['headers']).get(b'host', b'localhost:8000').decode()
        domain = f'{scheme}://{host_header}'
    else:
        domain = getattr(settings, 'DOMAIN', 'http://localhost:8000')

    return {
        'id': file.pk,
        'file': f'{domain}{file.file.url}',
        'type': file.type
    }


@database_sync_to_async
def get_file(pk=None):
    if pk is None:
        return None
    try:
        return File.objects.get(pk=pk)
    except File.DoesNotExist:
        return None
