import uuid

from django.conf import settings
from django.db import models

class Verify(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='verify', on_delete=models.CASCADE)