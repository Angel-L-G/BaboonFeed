# users/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import PublicUserSerializer, UserDetailSerializer, UserUpdateSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # GET /users/
    def list(self, request):
        username = request.query_params.get('username')
        if username:
            users = User.objects.filter(username__icontains=username)
            serializer = PublicUserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            users = User.objects.all()
            serializer = PublicUserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)

    # GET /users/<str:username>/
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UserDetailSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=["put"], url_path="me")
    def update_self(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
