import logging
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import F, Q
from django.urls import reverse

from rest_framework.authtoken.models import Token

logger = logging.getLogger('console-basic')

# ------------------------------------------------------------------------------------------------
#   --   MANAGERS    --

class UserManager(BaseUserManager):
    """Base class for users"""

    def create_user(self, email, username, password=None, **extra_fields):
        """Separating password so it will be encrypted"""
        if not email:
            raise ValueError('A valid email address is required')

        email = email.lower()
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Don't need the param '**extra_fields as the superuser will
        only be created in the command line.
        """
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class PublicUserManager(models.Manager):
    """Filter for only returning users that are active and not private"""

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_private=False) &
            Q(is_active=True)
        )

# ------------------------------------------------------------------------------------------------
#   --   USER MODELS    --

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using an email instead
    of a username."""
    email = models.EmailField(
        max_length=127,
        null=True,
        blank=True,
        unique=True,
    )
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField(default=uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    public = PublicUserManager()

    class Meta:
        ordering = ('username',)
        indexes = [
            models.Index(fields=['username']),
            ]

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        """Returns User Detail view"""
        return reverse("user:users-detail", kwargs={"pk": self.id})

    @classmethod
    def preload_related(cls):
        return cls.public.prefetch_related("profile").order_by('id')        


class Profile(models.Model):
    GENDERS = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=GENDERS
    )
    dob = models.DateField(null=True, blank=True)
    locale = models.CharField(max_length=100, default = '', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"