from .models import UserRoles
from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):
    '''
    admin: all
    owner: update, change_password, me
    authenticated: get
    any: create
    '''
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if (not request.user or not request.user.is_authenticated):
            return view.action == 'create'
        elif request.user.is_superuser or request.user.is_staff or request.user.role == UserRoles.ADMINISTRATOR:
            return True
        elif request.user == obj:
            return view.action not in ['list', 'delete', 'update_role']
        elif request.user.is_authenticated:
            return view.action in ['get', 'create']
        return False