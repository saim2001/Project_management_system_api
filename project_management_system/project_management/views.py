from rest_framework import generics,viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import Project,Task,ProjectPermission
from .permissions import IsProjectOwnerOrReadOnly,HasProjectPermission,CanAddUsers
from .serializer import UserSerializer,MyTokenObtainPairSerializer,ProjectSerializer,TaskSerializer,ProjectPermissionSerializer
from django.contrib.auth import get_user_model

User =  get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,IsProjectOwnerOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,HasProjectPermission]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ProjectPermissionView(generics.CreateAPIView):
    queryset = ProjectPermission.objects.all()
    serializer_class = ProjectPermissionSerializer
    permission_classes = [IsAuthenticated, CanAddUsers]
    




# Create your views here.
