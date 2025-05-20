from rest_framework import serializers
import mimetypes
from .models import File

class FileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'file', 'type']

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def validate_file(self, value):
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif',
            'audio/mpeg', 'audio/mp3', 'audio/wav',
            'video/mp4', 'video/webm', 'video/ogg'
        ]
        content_type = value.content_type
        if content_type not in allowed_types:
            raise serializers.ValidationError('Tipo de archivo no permitido.')
        return value
