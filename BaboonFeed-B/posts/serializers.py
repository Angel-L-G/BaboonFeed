from rest_framework import serializers

from files.models import File
from users.serializers import UserSerializer

from files.serializers import FileSerializer
from users.serializers import UserSerializer
from .models import Post, Reply

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Serializador anidado
    # Entrada: espera ID del archivo
    file_id = serializers.PrimaryKeyRelatedField(
        source='file',
        queryset=File.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    # Salida: muestra el archivo serializado
    file = FileSerializer(read_only=True)

    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at',
            'file_id',  # write-only
            'file',  # read-only
            'user',
            'likes_count', 'dislikes_count',
            'likes', 'dislikes'
        ]
        read_only_fields = ['user', 'likes', 'dislikes']  # No se pueden modificar estos campos

    def get_likes_count(self, obj):
        return obj.likes.count()  # Cuenta la cantidad de likes

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()  # Cuenta la cantidad de dislikes

class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()  # Campo para anidar respuestas
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['id', 'content', 'created_at', 'user', 'post', 'parent_reply', 'replies']
        read_only_fields = ['user', 'post', 'likes', 'dislikes']  # No se pueden modificar estos campos

    def get_replies(self, obj):
        """ Obtiene las respuestas hijas de esta respuesta """
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data

    def get_likes_count(self, obj):
        return obj.likes.count()  # Cuenta la cantidad de likes

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()  # Cuenta la cantidad de dislikes
