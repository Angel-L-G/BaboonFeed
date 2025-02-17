from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'  # Puedes personalizar los campos si prefieres
        read_only_fields = ['user', 'likes', 'dislikes']  # No se pueden modificar estos campos

    def get_likes_count(self, obj):
        return obj.likes.count()  # Cuenta la cantidad de likes

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()  # Cuenta la cantidad de dislikes
