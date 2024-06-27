from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedAndVerifiedOrNot(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_verified and request.method == "GET":
            return True
        elif request.user.is_staff:
            return True
        return False
