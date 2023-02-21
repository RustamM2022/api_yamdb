from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import CommentSerializer, ReviewSerializer
from users.permissions import IsSuperUserIsAdminIsModeratorIsAuthor

from reviews.models import Review, Title, Comments


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsSuperUserIsAdminIsModeratorIsAuthor,)

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        # Получаем id котика из эндпоинта
        title_id = self.kwargs.get("title_id")
        # И отбираем только нужные комментарии
        reviews = Review.objects.filter(title=title_id)
        return reviews 
    
    # def get_queryset(self):
    #    return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsSuperUserIsAdminIsModeratorIsAuthor,)

    # вернет отзыв
    def get_review(self):
        review =  get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review

    # Получаем все комменты произведения
    def get_queryset(self):
        # Получаем id котика из эндпоинта
        review_id = self.kwargs.get("review_id")
        # И отбираем только нужные комментарии
        comments = Comments.objects.filter(review=review_id)
        return comments

    # def get_queryset(self):
    #    return self.get_review().comments.all()

    # создаст коммент, если соблюдены условия
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
