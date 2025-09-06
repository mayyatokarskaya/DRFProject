from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверка, что пользователь — владелец объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(BasePermission):
    """Проверка, что пользователь в группе moderators"""

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="moderators").exists()

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.groups.filter(name="moderators").exists()


class IsOwnerOrModerator(BasePermission):
    """Проверка, что пользователь — владелец объекта ИЛИ модератор"""

    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner == request.user
        is_moderator = request.user.groups.filter(name="moderators").exists()
        return is_owner or is_moderator


class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.groups.filter(name="moderators").exists() or request.user.is_staff)
