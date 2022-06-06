import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    SUPERUSER = 'superuser'

    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
        (SUPERUSER, 'Суперпользователь')
    ]

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True, null=True,)
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(max_length=256, default=uuid.uuid4)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or 'superuser'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
