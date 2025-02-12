from django.db import models

class File(models.Model):
    class Type(models.TextChoices):
        AUDIO = 'audio'
        IMAGE = 'image'
        VIDEO = 'video'

    file = models.FileField(upload_to='files')
    type = models.CharField(max_length=5, choices=Type, null=True)

    def __str__(self):
        return self.file.url