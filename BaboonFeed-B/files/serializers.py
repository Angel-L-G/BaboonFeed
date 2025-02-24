from rest_framework import serializers
import mimetypes
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'type']

    def validate_file(self, value):
        mime_type, _ = mimetypes.guess_type(value.name)
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif',
            'audio/mpeg', 'audio/mp3', 'audio/wav',
            'video/mp4', 'video/webm', 'video/ogg'
        ]
        if mime_type not in allowed_types:
            raise serializers.ValidationError('Tipo de archivo no permitido.')
        return value
