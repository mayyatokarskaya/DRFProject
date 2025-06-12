from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Проверка, что пользователь — владелец объекта"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModerator(BasePermission):
    """Проверка, что пользователь в группе moderators"""
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="moderators").exists()
