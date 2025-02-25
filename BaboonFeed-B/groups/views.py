from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import GroupChat
from .serializers import GroupChatSerializer
from .permissions import IsGroupLeader

class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated, IsGroupLeader]  # Se requiere estar autenticado y ser líder para hacer modificaciones

    def perform_create(self, serializer):
        """Al crear un grupo, el usuario que lo crea será automáticamente el líder."""
        serializer.save(leader=self.request.user)

    def get_queryset(self):
        """
        Filtra los grupos para que el usuario solo vea los grupos donde es líder o miembro.
        """
        user = self.request.user
        return GroupChat.objects.filter(members=user).union(
            GroupChat.objects.filter(leader=user)
        )

    def perform_update(self, serializer):
        """
        Solo el líder actual puede modificar el grupo.
        """
        group = self.get_object()
        if self.request.user != group.leader:
            raise PermissionDenied("Solo el líder puede modificar el grupo.")
        serializer.save()

