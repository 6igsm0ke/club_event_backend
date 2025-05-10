from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsClubOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS — разрешены всем
        return getattr(request.user, "is_club_admin", False)  # Только клуб может создавать, изменять и удалять
