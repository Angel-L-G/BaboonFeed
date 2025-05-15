from django.conf import settings
from django.db import models

class GroupChat(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/group/', default='avatars/group/default.png')
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='groups_leadered', on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='member_of')
