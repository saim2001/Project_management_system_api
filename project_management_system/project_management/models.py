from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    pass

class Project(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='projects')

    def __str__(self) -> str:
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ProjectPermission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add_users = models.BooleanField(default=False)

    
