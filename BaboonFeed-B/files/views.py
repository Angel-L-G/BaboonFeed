from rest_framework import viewsets
from .models import File
from .serializer import FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
