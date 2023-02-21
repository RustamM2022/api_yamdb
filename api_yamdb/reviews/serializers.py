from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Comments, Review, Title


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
        # 'Рейтинг',
        default = '1',
        validators=[
            MinValueValidator(limit_value=1,
                              message='Минимальный рейтинг - 1'),
            MaxValueValidator(limit_value=10,
                              message='Максимальный рейтинг - 10')
        ],
    )

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title_id=title.id,
                                     author=author).exists():
                raise ValidationError('Может существовать только один отзыв!')
        return data
    
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date', 'score')
