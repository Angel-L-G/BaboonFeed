from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
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

    def create(self, request, *args, **kwargs):
        usernames = request.data.get('members', [])
        if not isinstance(usernames, list) or len(usernames) != 1:
            raise ValidationError({"detail": "Debe enviarse un solo username en 'members'."})

        target_username = usernames[0]
        current_user = request.user

        if target_username == current_user.username:
            raise ValidationError({"detail": "No puedes crear un chat contigo mismo."})

        target_user = get_object_or_404(User, username=target_username)

        existing_chat = Chat.objects.filter(members=current_user).filter(members=target_user).distinct()

        if existing_chat.exists():
            serializer = self.get_serializer(existing_chat.first())
            return Response(serializer.data, status=status.HTTP_200_OK)

        chat = Chat.objects.create()
        chat.members.add(current_user, target_user)
        chat.save()

        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
