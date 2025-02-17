from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import File
from .serializers import FileSerializer
import mimetypes
from rest_framework.response import Response

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
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        file_data = request.FILES['file']
        mime_type, _ = mimetypes.guess_type(file_data.name)

        if mime_type:
            if mime_type.startswith('image'):
                file_type = 'image'
            elif mime_type.startswith('video'):
                file_type = 'video'
            elif mime_type.startswith('audio'):
                file_type = 'audio'
            else:
                file_type = 'unknown'
        else:
            file_type = 'unknown'

        file = File.objects.create(file=file_data, type=file_type)
        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # No permitido
    def update(self, request, *args, **kwargs):
        pass

    # No permitido
    def partial_update(self, request, *args, **kwargs):
        pass

    # Destruir un archivo
    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]  # Necesita token
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)
