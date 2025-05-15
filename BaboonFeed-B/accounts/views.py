from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer


class RegisterViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(serializer.validated_data)

        # Generar tokens para el usuario recién creado
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "refresh": str(refresh),
            "access": access_token
        }, status=status.HTTP_201_CREATED)