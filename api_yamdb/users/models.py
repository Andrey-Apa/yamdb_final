import uuid

from django.contrib.auth.models import AbstractUser

from django.db import models

from .validators import validate_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_login_fields'
            ),
        )
