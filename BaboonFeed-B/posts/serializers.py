from rest_framework import serializers

from files.serializers import FileSerializer
from .models import Post, Reply

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    file = FileSerializer()

    class Meta:
        model = Post
        fields = '__all__'  # Puedes personalizar los campos si prefieres
        read_only_fields = ['user', 'likes', 'dislikes']  # No se pueden modificar estos campos

    def get_likes_count(self, obj):
        return obj.likes.count()  # Cuenta la cantidad de likes

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()  # Cuenta la cantidad de dislikes

class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()  # Campo para anidar respuestas

    class Meta:
        model = Reply
        fields = ['id', 'content', 'created_at', 'user', 'post', 'parent_reply', 'replies']
        read_only_fields = ['user', 'post']  # No se pueden modificar estos campos

    def get_replies(self, obj):
        """ Obtiene las respuestas hijas de esta respuesta """
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data
