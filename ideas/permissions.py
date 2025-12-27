from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Permission to allow only authors of an idea to edit it.
    Read-only requests are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if request method is safe (GET, HEAD, OPTIONS),
        or if the user is the author of the idea.
        """
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "author"):
            return obj.author == request.user

        return False
