from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shared.views import CustomLimitOffsetPagination
from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer


class ChatViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar los chats entre usuarios.
    """
    queryset = Chat.objects.all().order_by('-last_modified')
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtra los chats por el usuario autenticado.
        """
        user = self.request.user
        return Chat.objects.filter(members__in=[user])

    @action(detail=True, methods=["get"], url_path="messages")
    def messages(self, request, pk=None):
        """
        GET /api/chats/<id>/messages/?limit=20&offset=0
        Devuelve los mensajes más recientes primero (scroll hacia arriba).
        """
        chat = self.get_object()

        if request.user not in chat.members.all():
            return Response({"detail": "No autorizado."}, status=403)

        messages = chat.messages.all().order_by("-created_at")

        paginator = CustomLimitOffsetPagination()
        paginated_qs = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user) | Message.objects.filter(receiver=self.request.user)
