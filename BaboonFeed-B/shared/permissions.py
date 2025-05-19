from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite lectura a todos, pero solo el dueño del post puede eliminarlo.
    """

    def has_object_permission(self, request, view, obj):
        # Permitir GET, HEAD, y OPTIONS a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'PATCH' and  hasattr(view, 'action') and view.action in ['like', 'dislike']:
            return True

        # Permitir eliminar o crear el like solo al dueño del post
        if request.method in ['DELETE', 'POST']:
            return obj.user == request.user

        # Bloquear cualquier otra acción (PUT)
        return False

class UserViewsetPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Permitir lectura solo de la url GET /users/{username}/
        if request.method == 'GET' and  hasattr(view, 'action') and view.action in ['']:
            return True

        return False