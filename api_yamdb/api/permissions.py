from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Права администратора."""

    message = 'Недостаточно прав, вы не администратор!'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.is_admin)
                )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права администратора или только чтение."""

    message = 'Недостаточно прав, вы не администртор!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.is_admin)
                    )
                )


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Права автора, администратора, модератора или только чтение."""

    message = 'Недостаточно прав, аутентифицируйтесь!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.is_admin
                         or request.user.is_moderator
                         or request.user == obj.author)
                    )
                )
