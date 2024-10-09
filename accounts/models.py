from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class CustomUser(AbstractUser):
    credit = models.IntegerField(default=0)
