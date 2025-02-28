from django.contrib.auth import get_user_model
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
