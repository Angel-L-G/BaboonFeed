import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.aggregates import Count
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from chats.models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.isPrivate = self.scope["path"].find("private") != -1
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] if not self.isPrivate else f'user_{self.scope["url_route"]["kwargs"]["room_name"]}'
        self.room_group_name = f"chat_{self.room_name}"

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

        if self.isPrivate:
            receiver = await self.get_user(username=message["receiver"])
            group = None
            chat = await self.get_or_create_private_chat(self.user, receiver)
        else:
            receiver = None
            group = await self.get_user(id=self.room_name)

        new_message = await sync_to_async(Message.objects.create)(
            content=message["content"],
            author=self.user,
            receiver=receiver,
            group=group
        )

        if self.isPrivate:
            # Actualizar el último mensaje del chat
            chat.last_message = new_message
            sync_to_async(chat.save)()

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
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