from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        """
        Filtra los chats por el usuario autenticado.
        """
        user = self.request.user
        return user.chats.all()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user) | Message.objects.filter(receiver=self.request.user)
