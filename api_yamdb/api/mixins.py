from rest_framework import mixins, viewsets

from .permissions import IsAdminOrReadOnly


class ListCreateDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Базовый класс для вьюсетов категорий и жанров.
    Настроен поиск по полю 'name'.
    """
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
