
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from django.utils.timezone import now

class UserRoles(models.IntegerChoices):
    ADMINISTRATOR = (0, 'Administrator')
    INSTRUCTOR = (1, 'Instructor')
    MODERATOR = (2, 'Moderator')
    STUDENT = (3, 'Student')

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4)
    email = models.EmailField(_("email address"), unique=True)
    role = models.IntegerField(choices=UserRoles.choices, default=UserRoles.STUDENT)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}> ({self.role})"
    
    