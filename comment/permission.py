from rest_framework.permissions import BasePermission , SAFE_METHODS



class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool (
            request.user.is_superuser or request.user.is_shopadmin or obj.user == request.user
        )

  
     