from rest_framework import serializers

from users.serializers import UserSerializer

from files.serializers import FileSerializer
from users.serializers import UserSerializer
from .models import Post, Reply

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Serializador anidado
    user = UserSerializer(read_only=True)  # Serializador anidado
    file = FileSerializer()

    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'  # Incluye todos los campos del modelo
        read_only_fields = ['user']  # No se pueden modificar estos campos
        fields = '__all__'  # Incluye todos los campos del modelo
        read_only_fields = ['user']  # No se pueden modificar estos campos

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
        read_only_fields = ['user', 'post']  # No se pueden modificar estos campos

    def get_replies(self, obj):
        """ Obtiene las respuestas hijas de esta respuesta """
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data

    def get_likes_count(self, obj):
        return obj.likes.count()  # Cuenta la cantidad de likes

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()  # Cuenta la cantidad de dislikes
