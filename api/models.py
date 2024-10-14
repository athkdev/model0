import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50)


    def __str__(self):
        return self.email

    # override the save method, to set the email same as username
    def save(self, *args, **kwargs):
        if self.username:
            self.email = self.username

        super().save(*args, **kwargs)