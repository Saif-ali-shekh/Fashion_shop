from rest_framework.permissions import BasePermission

class IsCustomerOwner(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.type=='customer'
            
            
class IsOwnerUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.type=='Owner'