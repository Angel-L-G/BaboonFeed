from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from shared.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Permite lectura a todos, pero escritura solo a autenticados

    def perform_create(self, serializer):
        """
        Asigna el usuario autenticado al crear un post.
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Al eliminar un usuario, asigna 'deleted' en vez de eliminarlo.
        """
        post = self.get_object()
        post.user = get_object_or_404(get_user_model(), username='deleted')
        post.save()
        return Response({"mensaje": "El usuario del post ha sido cambiado a 'deleted'."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Permite a un usuario dar like a un post.
        Si ya ha dado dislike, lo elimina.
        """
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"mensaje": "Like eliminado"}, status=status.HTTP_200_OK)

        post.dislikes.remove(user)  # Si el usuario ya dio dislike, lo eliminamos
        post.likes.add(user)
        return Response({"mensaje": "Post likeado"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        """
        Permite a un usuario dar dislike a un post.
        Si ya ha dado like, lo elimina.
        """
        post = self.get_object()
        user = request.user

        if user in post.dislikes.all():
            post.dislikes.remove(user)
            return Response({"mensaje": "Dislike eliminado"}, status=status.HTTP_200_OK)

        post.likes.remove(user)  # Si el usuario ya dio like, lo eliminamos
        post.dislikes.add(user)
        return Response({"mensaje": "Post dislikeado"}, status=status.HTTP_200_OK)
