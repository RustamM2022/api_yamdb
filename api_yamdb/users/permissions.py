from rest_framework import permissions


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    """
    Предоставляет права на запр.
    только сп , админу Джанго или
    аун. пользователю с ролью admin.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.role == 'admin')
        )


class AnonimReadOnly(permissions.BasePermission):
    """Разрешает анониниму безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """
    Разрешает анониму безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    сп Джанго, админу Джанго, аут пользователям
    с ролью admin или moderator, а также автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.role == 'admin'
                 or request.user.role == 'moderator'
                 or request.user == obj.author)
        )
