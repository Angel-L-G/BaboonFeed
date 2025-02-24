from rest_framework import viewsets, permissions
from .models import Messages
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Messages.objects.filter(author=self.request.user) | Messages.objects.filter(receiver=self.request.user)
