import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.aggregates import Count
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from chats.models import Message, Chat
from groups.models import GroupChat


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_user = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_user_{self.room_user}"

        # Realizar la autenticación con el token recibido
        self.token = None
        self.user = AnonymousUser()

        # Únete al grupo de WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

        # Esperar el primer mensaje para autenticar
        if message.get("type") == "auth" and message.get("token"):
            access_token = AccessToken(message["token"])
            self.user = await self.get_user(id=access_token["user_id"])
            return

        # Si no se autenticó correctamente, cerrar la conexión
        if self.user == AnonymousUser():
            await self.close()

        receiver = await self.get_user(username=message["receiver"])
        chat = await self.get_or_create_private_chat(self.user, receiver)

        new_message = await sync_to_async(Message.objects.create)(
            content=message["content"],
            author=self.user,
            receiver=receiver,
            chat=chat
        )

        chat.last_message = new_message
        sync_to_async(chat.save)

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

        await self.channel_layer.group_send(
            f'chat_user_{message["receiver"]}',
            {
                "type": "chat_message",
                "message": message
            }
        )

    @sync_to_async
    def get_or_create_private_chat(self, user1, user2):
        # Buscar un chat privado con exactamente esos 2 usuarios
        chat = Chat.objects.filter(
            users=user1
        ).filter(users=user2)

        if chat.exists():
            return chat.first()

        # Crear el chat si no existe
        chat = Chat.objects.create()
        chat.users.add(user1, user2)
        return chat

    async def chat_message(self, event):
        message = event["message"]

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({"message": message}))

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
        self.group_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_group_{self.group_id}"

        # Realizar la autenticación con el token recibido
        self.token = None
        self.user = AnonymousUser()

        # Únete al grupo de WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

        # Esperar el primer mensaje para autenticar
        if message.get("type") == "auth" and message.get("token"):
            access_token = AccessToken(message["token"])
            self.user = await self.get_user(id=access_token["user_id"])
            return

        # Si no se autenticó correctamente, cerrar la conexión
        if self.user == AnonymousUser():
            await self.close()

        group_chat = await self.get_group_chat(id=self.group_id)
        if group_chat is None:
            return

        new_message = await sync_to_async(Message.objects.create)(
            content=message["content"],
            author=self.user,
            group=group_chat
        )

        group_chat.last_message = new_message
        sync_to_async(group_chat.save)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        message = event["message"]

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({"message": message}))

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