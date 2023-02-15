from django.contrib.auth.models import AbstractUser
from django.db import models


Roles = (
        ('Anonym', 'Аноним'),
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
        ('superuser', 'Суперюзер'),
)


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        blank=True,
        max_length=254,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=Roles,
        max_length=30,
        default='user'
    )
