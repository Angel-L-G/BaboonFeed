from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shared.views import CustomLimitOffsetPagination

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


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

    from rest_framework.response import Response
    from django.utils.dateparse import parse_datetime

    @action(detail=True, methods=['get'], url_path='messages')
    def messages(self, request, pk=None):
        chat = self.get_object()

        if request.user not in chat.members.all():
            return Response({'detail': 'No autorizado.'}, status=403)

        queryset = chat.messages.all().order_by('-created_at')

        before = request.query_params.get('before')
        if before:
            before_dt = parse_datetime(before)
            if before_dt:
                queryset = queryset.filter(created_at__lt=before_dt)

        limit = int(request.query_params.get('limit', 20))
        messages = list(queryset[:limit + 1])

        has_more = len(messages) > limit
        messages = messages[:limit]

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response({
            'results': serializer.data,
            'has_more': has_more
        })

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user) | Message.objects.filter(
            receiver=self.request.user
        )
