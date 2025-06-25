from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, instance):
        if request.method != 'GET':
            if instance.owner == request.user:
                return True
            return False
        return True
