from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Comments, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'pub_date', 'author', 'review')
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    score = serializers.IntegerField(
        'Рейтинг',
        default = '1',
        validators=[
            MinValueValidator(limit_value=1,
                              message='Минимальный рейтинг - 1'),
            MaxValueValidator(limit_value=10,
                              message='Максимальный рейтинг - 10')
        ],
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date', 'score')
