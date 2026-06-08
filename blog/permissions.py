from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Allow read-only methods
        if request.method in SAFE_METHODS:
            return True
        
        # Admin override
        if request.user.is_staff:
            return True

        # Allow only owner
        return obj.author == request.user
    

class IsCommentOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read allowed
        if request.method in SAFE_METHODS:
            return True

        # Admin override
        if request.user.is_staff:
            return True

        # Only comment owner
        return obj.author == request.user
