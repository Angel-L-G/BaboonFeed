from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Verify
from accounts.serializers import RegisterSerializer
from accounts.utils import send_confirmation_email

User = get_user_model()


class RegisterViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Las contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(serializer.validated_data)
        send_confirmation_email(user, request)
        return Response({
            "message": "Check your email to confirm your account",
        }, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    def get(self, request, user_email, uid):
        decoded_email = urlsafe_base64_decode(user_email).decode()

        try:
            user = User.objects.get(email=decoded_email)
            verify_object = Verify.objects.get(user=user, hash=uid)
        except Verify.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
        if verify_object.is_expired():
            return Response({"error": "Token expired."}, status=status.HTTP_410_GONE)

        user.is_active = True
        user.save()
        Verify.objects.filter(user=user).delete()
        return Response({"message": "Activated account correctly."}, status=status.HTTP_200_OK)
