from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):

    category = filters.CharFilter(
        field_name='category__slug',
        search='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        search='icontains'
    )
    name = filters.CharFilter(
        field_name='name',
        search='contains'
    )
    year = filters.NumberFilter(
        field_name="year",
        search='exact'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
