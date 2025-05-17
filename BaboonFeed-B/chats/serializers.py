from rest_framework import serializers
from .models import Message, Chat

from users.models import User

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']

class ChatSerializer(serializers.ModelSerializer):
    members = ChatUserSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"