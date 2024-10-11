from rest_framework import permissions

"""
El permiso permite solo la lectura para todos los usuarios (GET),
pero solo los administradores pueden crear, actualizar o eliminar.
"""
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff