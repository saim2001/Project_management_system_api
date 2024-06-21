from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Task, ProjectPermission

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class ProjectSerializer(serializers.ModelSerializer):

    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), default=[])
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'created_by', 'is_deleted', 'users'
        )

        def create(self, validated_data):
            project = Project.objects.create(**validated_data)
            return project


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'project', 'title', 'description',
                  'status', 'due_date', 'is_deleted')


class ProjectPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPermission
        fields = ('user', 'can_create', 'can_edit',
                  'can_delete', 'can_add_users', 'project')
