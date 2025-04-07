from rest_framework import permissions

HTTP_DELETE = 'DELETE'

class IsGroupLeader(permissions.BasePermission):
    """
    Permite modificar un grupo solo si el usuario es el líder del grupo.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS or request.method == HTTP_DELETE:
            return request.user in obj.members.all() or request.user == obj.leader

        return obj.leader == request.user
