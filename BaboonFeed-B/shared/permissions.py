from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite lectura a todos, pero solo el dueño del post puede editarlo o eliminarlo.
    """

    def has_object_permission(self, request, view, obj):
        # Permitir GET, HEAD, y OPTIONS a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permitir eliminar pero NO actualizar
        if request.method in ['DELETE']:
            return obj.user == request.user

        # Bloquear cualquier otra acción (PUT/PATCH)
        return False
