# permissions.py
from rest_framework import permissions

class IsAdminAPI(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__iexact='admin').exists()


class IsAdminUser(permissions.BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class IsASMUser(permissions.BasePermission):
    """Allows access only to ASM users."""

    def has_permission(self, request, view):
        try:
            from .models import ASM
            ASM.objects.get(user=request.user)
            return True
        except ASM.DoesNotExist:
            return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allows access to object owners or admin users."""

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Check if the object belongs to the current ASM user
        try:
            from .models import ASM
            asm_profile = ASM.objects.get(user=request.user)

            # Handle different object types
            if hasattr(obj, 'asm') and obj.asm == asm_profile:
                return True
            if hasattr(obj, 'user') and obj.user == request.user:
                return True
            if hasattr(obj, 'asm_id') and obj.asm_id == asm_profile.id:
                return True

        except ASM.DoesNotExist:
            return False

        return False