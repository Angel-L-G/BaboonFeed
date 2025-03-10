import uuid
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

def default_expires_at():
    return now() + timedelta(hours=42)

class Verify(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='verify', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expires_at)  # Usar la función definida

    def is_expired(self):
        return now() > self.expires_at
