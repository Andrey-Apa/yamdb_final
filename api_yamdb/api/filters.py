from django_filters import rest_framework as filter

from reviews.models import Title


class TitleFilter(filter.FilterSet):
    """Фильтр для вьюсета произведений. Фильтрация по полям
    'genre', 'category', 'name', 'year'.
    """
    genre = filter.CharFilter(field_name='genre__slug')
    category = filter.CharFilter(field_name='category__slug')
    name = filter.CharFilter(field_name='name')
    year = filter.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year',)
