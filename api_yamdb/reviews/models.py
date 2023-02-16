from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from api.models import Title

class Review(models.Model):
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
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
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comments(models.Model):
    text = text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария',
        verbose_name = 'Комментарий'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('pub_date',)
