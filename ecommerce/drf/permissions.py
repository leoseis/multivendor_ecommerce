from rest_framework.permissions import BasePermission

class IsVendor(BasePermission):
    """
    Allows access only to vendor users
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            user.is_vendor
        )
