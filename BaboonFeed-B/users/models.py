from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class Follow(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['following', 'followed_by']

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/user', default='avatars/user/default.png')
    follows = models.ManyToManyField('self', related_name='follows_users', symmetrical=False, through=Follow)
    blocked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blocked_users')

# Follow.objects.filter(following=user.pk)
# Follow.objects.filter(followed_by=user.pk)