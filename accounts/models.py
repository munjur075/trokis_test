from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("The mobile number must be set")
        extra_fields.setdefault("is_active", False)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        
        if not password:
            raise ValueError("Superuser must have a password.")
        
        if extra_fields.get("is_verified") is not True:
            raise ValueError("Superuser must have is_verified=True.")
        
        if extra_fields.get("role") != "admin":
            raise ValueError("Superuser must have role='admin'.")
        
        return self.create_user(mobile_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('user', 'User'),
        ('guest', 'Guest'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    mobile_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expired = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.mobile_number
