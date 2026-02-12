from rest_framework.permissions import BasePermission

class IsVendor(BasePermission):
    message = "You must be a vendor to perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_vendor", False)
        )
