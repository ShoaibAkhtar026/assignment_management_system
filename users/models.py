import uuid as uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email
