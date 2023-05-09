import re

from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]

    def validate(self, data):
        if not re.match(r'^[\w.@+-]+', str(data.get('username'))):
            raise serializers.ValidationError(
                "Неверный формат имени."
            )
        return data


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]


class SignupSerializer(serializers.ModelSerializer):

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                'Полученный username уже используется другим '
                'пользователем.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                'Полученный email уже используется другим '
                'пользователем.')
        if data.get('username').lower() == 'me':
            raise serializers.ValidationError(
                f'Имя пользователя {username} недопустимо. '
                'Используйте другое имя.')
        if not re.match(r'^[\w.@+-]+', str(data.get('username'))):
            raise serializers.ValidationError(
                "Неверный формат имени."
            )
        return data

    class Meta:
        fields = ('username', 'email')
        model = User
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = (
            'username', 'confirmation_code',)
