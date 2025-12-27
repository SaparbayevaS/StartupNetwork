from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsUserOrReadOnly(BasePermission):
    """
    Permission to allow users to edit only their own data.
    Read-only requests are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if request method is safe (GET, HEAD, OPTIONS),
        or if the user is the owner of the object.
        """
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
