from rest_framework import permissions

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='user'):
            return True
        return False
    
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='manager'):
            return True
        return False