# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project, ProjectPermission
from django.conf import settings


class IsProjectOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow list and create actions without checking for a pk
        print(view.kwargs)
        if view.action in ['list', 'create']:
            return True

        # For detail views, check for permissions based on 'pk'
        if 'pk' in view.kwargs:
            try:
                project = Project.objects.get(id=view.kwargs['pk'])
            except Project.DoesNotExist:
                return False

            # Allow if the user is the creator of the project
            if project.created_by == request.user:
                return True

            # Otherwise, check specific permissions
            permission = ProjectPermission.objects.filter(
                project=project,
                user=request.user
            ).first()

            if permission:
                if view.action == 'retrieve' and permission.can_view:
                    return True
                if view.action == 'update' and permission.can_add_users:
                    return True

        return False


class HasProjectPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        
        if request.method == 'DELETE':
            task = Task.objects.get(id=view.kwargs['pk'])
            project_id = task.project.id
        else:

            try:
                project_id = request.data['project']
            except:
                project_id = view.kwargs['pk']
        

        try:
            print(project_id)
            project = Project.objects.get(id=project_id)
            print(request.user, project.created_by)
            if request.user == project.created_by:
                return True
            permission = ProjectPermission.objects.get(
                project=project, user=request.user)
        except Project.DoesNotExist:
            return False
        except ProjectPermission.DoesNotExist:
            return False

        if request.method == "POST" and permission.can_create:
            return True

        if request.method in ['PUT', 'PATCH'] and permission.can_edit:
            return True
        if request.method == 'DELETE' and permission.can_delete:
            return True
        return False

class CanAddPermissions(BasePermission):
    def has_permission(self, request, view):
        print(view.kwargs, request.user.id)
        project = Project.objects.get(id=request.data['project'])
        print(project.created_by)
        return project.created_by == request.user


class CanAddUsers(BasePermission):
    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['pk'])
        permission = ProjectPermission.objects.get(
            project=project, user=request.user)
        return permission.can_add_users
