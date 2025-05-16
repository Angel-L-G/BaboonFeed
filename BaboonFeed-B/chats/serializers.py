from rest_framework import serializers
from .models import Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"