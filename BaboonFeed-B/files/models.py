from django.db import models
from django.core.exceptions import ValidationError
import mimetypes

def validate_file_type(file):
    mime_type, _ = mimetypes.guess_type(file.name)
    allowed_types = [
        'image/jpeg', 'image/png', 'image/gif',
        'audio/mpeg', 'audio/ogg', 'audio/wav',
        'video/mp4', 'video/webm', 'video/ogg'
    ]
    if mime_type not in allowed_types:
        raise ValidationError('Tipo de archivo no permitido.')

class File(models.Model):
    class Type(models.TextChoices):
        AUDIO = 'audio'
        IMAGE = 'image'
        VIDEO = 'video'

    file = models.FileField(upload_to='files', validators=[validate_file_type])
    type = models.CharField(max_length=5, choices=Type, null=True)

    def __str__(self):
        return self.file.url