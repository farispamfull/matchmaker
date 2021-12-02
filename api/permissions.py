from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class AdminOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or request.user.is_staff
                or request.user.role == 'moderator')
