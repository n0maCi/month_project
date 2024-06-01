from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    password = models.CharField(("password"), max_length=128, null=True)
    username = models.CharField(max_length=150, null=True, unique=True)
    gender = models.CharField(max_length=20, null=True)
    birthday = models.CharField(max_length=20, null=True)
    residence_address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    residence_address = models.CharField(max_length=255, null=True)
