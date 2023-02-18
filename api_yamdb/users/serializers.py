from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
import re


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'bio', 'first_name', 'last_name', 'role')
        model = User
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]

    def validate(self, data):
        # if data.get('username') == 'me':
        #     raise serializers.ValidationError(
        #         'Имя пользователя me недопустимо. Используйте другое имя.')
        if not re.match(r'^[\w.@+-]+', str(data.get('username'))):
            raise serializers.ValidationError(
                "Неверный формат имени."
            )
        return data

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


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
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'Полученный username уже используется другим '
                'пользователем.')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Полученный email уже используется другим '
                'пользователем.')
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя me недопустимо. Используйте другое имя.')
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




        # if User.objects.filter(username=username).first() != User.objects.filter(email=email).first():
        #     raise ValidationError(
        #         'Полученный email или username уже используется другим '
        #         'пользователем.')



# class SignupSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(min_length=8, write_only=True)

#     class Meta:
#         fields = ('username', 'email', 'password', 'id')
#         model = User
#         validators = [UniqueTogetherValidator(
#             queryset=User.objects.all(),
#             fields=('username', 'email')
#         )
#         ]

#     def validate(self, data):
#         if data.get('username') == 'me':
#             raise serializers.ValidationError(
#                 'Имя пользователя me недопустимо. Используйте другое имя.')
#         if not re.match(r'^[\w.@+-]+', str(data.get('username'))):
#             raise serializers.ValidationError(
#                 "Неверный формат имени."
#             )
#         return data

#     def validate_password(self, email, password):
#         try:
#             self.user = User.objects.get(email=email)
#         except ObjectDoesNotExist:
#             message = {'error': f'User with email={email} does not exist.'}
#             return message
#         check_auth = authenticate(username=email, password=password)
#         if check_auth is None:
#             message = {'error':
#                        'The user exists, but the password is incorrect.'}
#             return message
#         data = self.user.jwt_tokens
#         update_last_login(None, self.user)
#         return data


# class TokenSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(min_length=8, write_only=True)

#     def validate(self, email, password):
#         try:
#             self.user = User.objects.get(email=email)
#         except ObjectDoesNotExist:
#             message = {'error': f'User with email={email} does not exist.'}
#             return message
#         check_auth = authenticate(username=email, password=password)
#         if check_auth is None:
#             message = {'error':
#                        'The user exists, but the password is incorrect.'}
#             return message
#         data = self.user.jwt_tokens
#         update_last_login(None, self.user)
#         return data
