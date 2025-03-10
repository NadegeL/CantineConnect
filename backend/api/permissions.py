from rest_framework import permissions


class IsParentUser(permissions.BasePermission):
    """
    Customized permission to allow only 'parent' users to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'parent'

    def has_object_permission(self, request, view, obj):
        # Make sure the user can only access his own profile
        return obj.user == request.user
