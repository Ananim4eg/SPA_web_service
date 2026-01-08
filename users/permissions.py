from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Разрешает доступ только пользователям из группы «moderator»"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()