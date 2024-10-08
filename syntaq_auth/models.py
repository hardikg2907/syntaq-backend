from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from uuid import uuid4


class CustomUserModelManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a regular user"""
        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, **extra_fields)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    userId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=16, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField()

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["email"]

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserModelManager()

    class Meta:
        verbose_name = "Custom User"

    def __str__(self):
        return self.username
