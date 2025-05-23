from django.conf import settings
from django.db import models

class Chat(models.Model):
    last_modified = models.DateTimeField(auto_now=True)
    last_message = models.ForeignKey(
        'chats.Message',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='last_used_in_chat'
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_sended', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_received', on_delete=models.CASCADE, null=True, blank=True)
    chat = models.ForeignKey('chats.Chat', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey('groups.GroupChat', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey('files.File', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)