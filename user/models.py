from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True, null=True)
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=60)
    username = models.CharField(max_length=40, unique=False, default='')
    address = models.CharField(max_length=300, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
