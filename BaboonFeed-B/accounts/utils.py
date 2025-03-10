from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.models import Verify


def send_confirmation_email(user, request):
    verify = Verify.objects.create(user=user)
    user_email = urlsafe_base64_encode(force_bytes(user.email))  # 🔥 CORREGIDO
    confirm_url = request.build_absolute_uri(f"/api/verify-email/{user_email}/{verify.hash}/")

    subject = "Confirm your account"
    message = f"Hello, {user.username}.\nPlease confirm your account so you can access our awesome social media. Click the link below to confirm:\n\n{confirm_url}"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
