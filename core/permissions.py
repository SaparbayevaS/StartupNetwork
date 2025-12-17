from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Permissions to allow owners of an object to edit it.
    Read onlu requests are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if request is a safe method (get, head, options),
        or if the user is the author of the object.
        """
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "author"):
            return obj.author == request.user


        return False
