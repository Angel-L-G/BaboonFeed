from django.conf import settings
from django.db import models

class Messages(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_sended', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_received', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey('groups.Group', related_name='messages', on_delete=models.CASCADE, null=True)