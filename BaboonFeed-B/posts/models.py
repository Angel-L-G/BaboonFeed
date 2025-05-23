from django.conf import settings
from django.db import models

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.OneToOneField('files.File', related_name='post', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.DO_NOTHING) # se controla en la view (ponerlo al usuario 'deleted')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_posts')

    def __str__(self):
        return self.content

class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_reply = models.ForeignKey(  # Cambio de nombre
        'self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True
    )
    post = models.ForeignKey('posts.Post', related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='replies', on_delete=models.DO_NOTHING) # se controla en la view (ponerlo al usuario 'deleted')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_replies')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_replies')

    def __str__(self):
        return self.content