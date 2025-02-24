from rest_framework import permissions


class IsGroupLeader(permissions.BasePermission):
    """
    Permite modificar un grupo solo si el usuario es el líder del grupo.
    """

    def has_object_permission(self, request, view, obj):
        # Permite GET a todos los usuarios
        if request.method in permissions.SAFE_METHODS:
            if request.user in obj.members.all() or request.user == obj.leader:
                return True
            return False

        # Solo el líder puede modificar el grupo
        return obj.leader == request.user
