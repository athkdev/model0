import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from .helpers import Helper

# Create your models here.


class User(AbstractUser):
    id = Helper.generate_uuid()
    role = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

    # override the save method, to set the email same as username
    def save(self, *args, **kwargs):
        if self.username:
            self.email = self.username

        super().save(*args, **kwargs)


class Project(models.Model):
    id = Helper.generate_uuid()
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # is models.DO_NOTHING a better choice?
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class SMModel(models.Model):
    id = Helper.generate_uuid()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True)
    aws_arn = models.CharField(max_length=255, blank=True)
    endpoint_name = models.CharField(max_length=255, blank=True)
    endpoint_config_name = models.CharField(max_length=255, blank=True)
    is_deployed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
