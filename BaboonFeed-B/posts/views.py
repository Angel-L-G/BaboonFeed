from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from shared.permissions import IsOwnerOrReadOnly
from .models import Post, Reply
from .serializers import PostSerializer, ReplySerializer


class PostLimitOffsetPagination(LimitOffsetPagination):
    """
    Clase de paginación para los posts.
    Permite paginar los resultados con un límite y un desplazamiento.
    """
    default_limit = 10
    max_limit = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Permite lectura a todos, pero escritura solo a autenticados
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por usuario si se pasa en la URL como ?user_id=1
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = self.queryset.filter(author_id=user_id)

        # Filtrar por el usuario autenticado si se pasa en la URL como ?followed=true
        followed = self.request.query_params.get("followed")
        if followed:
            queryset = queryset.filter(author__followers__in=[self.request.user])


        return queryset

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

    @action(detail=True, methods=['get', 'post'], url_path='replies')
    def replies(self, request, pk=None):
        post = self.get_object()

        if request.method == 'GET':
            """
            Retorna todas las respuestas de un post, incluyendo respuestas anidadas.
            """
            replies = post.replies.filter(parent_reply__isnull=True)  # Solo respuestas principales
            serializer = ReplySerializer(replies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            """
            Crea una respuesta a un post o dentro de otra respuesta.
            """
            serializer = ReplySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Obtener la respuesta padre si se envió un parent_reply
            parent_reply = None
            parent_reply_id = request.data.get('parent_reply')
            if parent_reply_id:
                parent_reply = get_object_or_404(Reply, id=parent_reply_id)

            serializer.save(user=request.user, post=post, parent_reply=parent_reply)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='replies/(?P<reply_pk>[^/.]+)')
    def delete_reply(self, request, pk=None, reply_pk=None):
        """
        Elimina una respuesta a un post.
        """
        post = self.get_object()
        reply = get_object_or_404(post.replies, pk=reply_pk)
        reply.user = get_object_or_404(get_user_model(), username='deleted')
        reply.save()
        return Response({"mensaje": "Respuesta eliminada"}, status=status.HTTP_200_OK)