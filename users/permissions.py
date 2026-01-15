from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Разрешает доступ только пользователям из группы «moderator»"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(permissions.BasePermission):
    """Разрешает доступ только к своим объектам"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
