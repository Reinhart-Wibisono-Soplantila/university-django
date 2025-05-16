from rest_framework.permissions import BasePermission

class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.filter.groups(name='Admin').exists()
        )
    
class isAdminStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.filter.groups(name='Administrative Staff').exists()
        )
    
class isStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.filter.groups(name='Student').exists()
        )
    
class isTeachingStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.filter.groups(name='Teaching Staff').exists()
        )