from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # All permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user