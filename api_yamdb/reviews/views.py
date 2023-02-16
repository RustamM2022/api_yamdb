from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer,ReviewSerializer
from откуда-то.permissions import 'авторпользовательадминчтение'

from reviews.models import Review, Title
from users.models import User 


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ('авторпользовательадминчтение',)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title.id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ('авторпользовательадминчтение',)

    # вернет отзыв
    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review.id'))

    # Получаем все комменты произведения
    def get_queryset(self):
        return self.get_review().comments.all()

    # создаст коммент, если соблюдены условия
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
