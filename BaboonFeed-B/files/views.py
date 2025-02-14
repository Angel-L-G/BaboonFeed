from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import File
from .serializers import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    # Listar todos los archivos
    def list(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]  # Público
        return super().list(request, *args, **kwargs)

    # Ver un archivo en específico
    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]  # Público
        return super().retrieve(request, *args, **kwargs)

    # Subir un nuevo archivo
    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # Necesita token
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    # Actualizar un archivo
    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # Necesita token
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)

    # No permitido
    def partial_update(self, request, *args, **kwargs):
        pass

    # Destruir un archivo
    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # Necesita token
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)
