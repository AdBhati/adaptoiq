from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TimeAudit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Custom user manager for handling user creation"""

    def create_user(self, email, username, password=None, role="Candidate"):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role, is_staff=False, is_superuser=False)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Create and return a superuser"""
        user = self.create_user(email, username, password, role="HR")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""

    ROLE_CHOICES = [
        ('HR', 'HR'),
        ('Candidate', 'Candidate'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"


