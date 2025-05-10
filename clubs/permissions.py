from rest_framework.permissions import BasePermission, SAFE_METHODS

class ClubEventPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        role_codes = user.rolerelated_set.values_list("role__code", flat=True)

        if request.method in SAFE_METHODS:
            return True  

        return "CLB" in role_codes  

