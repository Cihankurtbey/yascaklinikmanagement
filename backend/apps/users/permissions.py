from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission class: Admin can do everything, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_admin


class IsDoctorOrAdmin(permissions.BasePermission):
    """Permission class: Only doctors and admins"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_admin)


class IsAssistantOrAbove(permissions.BasePermission):
    """Permission class: Assistant, Doctor, or Admin"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
