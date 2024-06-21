from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, MyTokenObtainPairView, ProjectViewSet, TaskViewSet, ProjectPermissionViewSet
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'projectpermissions', ProjectPermissionViewSet)
urlpatterns += router.urls
