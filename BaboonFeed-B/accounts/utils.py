from django.conf import settings
from django.core.mail import send_mail

from accounts.models import Verify


def send_confirmation_email(user, request):
    verify = Verify.objects.create(user=user)
    confirm_url = request.build_absolute_uri(f"/verify-email/{user.email}/{verify.hash}/")
    subject = "Confirm your account"
    message = f'Hello, {user.username}.\nPlease confirm your account so you can access our awesome social media. Access to this link to confirm your account:\n\n{confirm_url}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)