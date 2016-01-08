from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):
    """
    A permission class responsible for allowing access to admin user for all the actions: create/view/update/delete
    and restricting other users to view only action.
    """
    def has_permission(self, request, view):
        if not request.user.is_staff and not request.method in permissions.SAFE_METHODS:
            return False
        return True


