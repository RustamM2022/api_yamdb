from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать это имя запрещено')
        return data


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('username', 'email')
        )
        ]
