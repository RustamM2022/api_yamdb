from django.db.models import Avg
from rest_framework import viewsets, filters
from reviews.models import Category, Genre, Title
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from users.permissions import (
    AnonimReadOnly,
    IsSuperUserOrIsAdminOnly
)
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleGETSerializer, TitleSerializer)
from rest_framework.pagination import PageNumberPagination


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitleSerializer
    permission_classes = (AnonimReadOnly | IsSuperUserOrIsAdminOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
