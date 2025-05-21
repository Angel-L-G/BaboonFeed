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

    # PUT /users/<str:username>/
    def update(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        logged_user = request.user
        if user != logged_user:
            return Response({"error": "You can only update your own profile."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserUpdateSerializer(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # PATCH /users/<str:username>/follow/
    @action(detail=True, methods=['patch'])
    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(User, username=pk)
        logged_user = request.user
        if logged_user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_follow in logged_user.follows.all():
            logged_user.follows.remove(user_to_follow)
        else:
            logged_user.follows.add(user_to_follow)
        return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
