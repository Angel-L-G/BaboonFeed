from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from shared.permissions import UserViewsetPermission
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, UserViewsetPermission]  # Permite lectura a todos, pero escritura solo a autenticados

    # GET /user/username/
    @action(methods=['get'], url_path='username')
    def get_user_data(self, serializer, username=None):
        """
        Obtiene los datos del usuario.
        """
        user = User.objects.filter(username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
