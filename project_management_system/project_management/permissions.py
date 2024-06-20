# permissions.py
from rest_framework.permissions import BasePermission,SAFE_METHODS
from .models import Project, ProjectPermission
from django.conf import settings

class IsProjectOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
       
        # Allow read-only access for non-authenticated users
        if request.method in SAFE_METHODS:
            return True
        # Check if the user is the owner of the project
        project = Project.objects.get(id=view.kwargs['pk'])
        return project.created_by == request.user

class HasProjectPermission(BasePermission):
    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['pk'])
        permission = ProjectPermission.objects.get(project=project, user=request.user)
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST' and permission.can_create:
            return True
        if request.method in ['PUT', 'PATCH'] and permission.can_edit:
            return True
        if request.method == 'DELETE' and permission.can_delete:
            return True
        return False

class CanAddUsers(BasePermission):
    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['pk'])
        permission = ProjectPermission.objects.get(project=project, user=request.user)
        return permission.can_add_users
