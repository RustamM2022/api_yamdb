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
    first_name = models.CharField(('first name'), max_length=150, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=Roles,
        max_length=30,
        default='user'
    )
