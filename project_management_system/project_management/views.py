from rest_framework import generics, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task, ProjectPermission
from .permissions import IsProjectOwnerOrReadOnly, HasProjectPermission, CanAddUsers, CanAddPermissions
from .serializer import UserSerializer, MyTokenObtainPairSerializer, ProjectSerializer, TaskSerializer, ProjectPermissionSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]

    def perform_create(self, serializer):
        users = serializer.validated_data.get('users', [])
        user = self.request.user
        users.append(user)
        project = serializer.save(created_by=user)
        project.users.set(users)
        for i in users:
            if i.id != user.id:
                part_usr = User.objects.get(id=i.id)
                permissions = ProjectPermission.objects.create(
                    project=project, user=part_usr)
                permissions.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasProjectPermission]

    # def perform_create(self, serializer):
    #     project_id = serializer.validated_data.get('project').id
    #     user_id = self.request.user.id
    #     try:
    #         project = Project.objects.get(id=project_id)
    #     except Project.DoesNotExist:
    #         raise NotFound('Project not found')
    #     print(self.request.user == project.created_by)
    #     if self.request.user == project.created_by:
    #         serializer.save()
    #     else:
    #         try:
    #             project_permission = ProjectPermission.objects.get(
    #                 project_id=project_id, user_id=user_id)
    #             if project_permission.can_create:
    #                 serializer.save()
    #             else:
    #                 raise PermissionDenied(
    #                     'You do not have permission to create task')
    #         except ProjectPermission.DoesNotExist:
    #             raise PermissionDenied(
    #                 'You do not have permission to create task')

    def perform_destroy(self, instance):

        instance.is_deleted = True
        instance.save()


class ProjectPermissionViewSet(viewsets.ModelViewSet):
    queryset = ProjectPermission.objects.all()
    serializer_class = ProjectPermissionSerializer
    permission_classes = [IsAuthenticated, CanAddPermissions]

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.request.data['project'])
        serializer.save(project=project)


# Create your views here.
