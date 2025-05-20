from django.template.context_processors import request
from rest_framework import serializers

from files.serializers import FileSerializer
from users.models import User

from .models import Chat, Message


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']


class ChatSerializer(serializers.ModelSerializer):
    members = ChatUserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'

    def get_last_message(self, obj):
        return obj.last_message.content if obj.last_message else None


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.username if obj.author else None

    def get_receiver(self, obj):
        return obj.receiver.username if obj.receiver else None

    def get_file(self, obj):
        if not obj.file:
            return None

        request = self.context.get('request')
        file_url = obj.file.file.url
        if request:
            file_url = request.build_absolute_uri(file_url)

        return {
            'id': obj.file.id,
            'file': file_url,
            'type': obj.file.type
        }
