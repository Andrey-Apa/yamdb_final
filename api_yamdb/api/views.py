from http import HTTPStatus
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg

from rest_framework import (filters, generics, response, viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (
    UserCreateSerializer, CustomTokenObtainSerializer, UserSerializer,
    CategorySerializer, GenreSerializer, ReadTitleSerializer,
    WriteTitleSerializer, ReviewSerializer, CommentSerializer
)
from reviews.models import User, Category, Genre, Title, Review


ALLOWED_METHODS = ('get', 'post', 'patch', 'delete')


class UserCreateViewSet(generics.CreateAPIView):
    """Представление для создания пользователя. Имеет только POST запрос.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        username = request.data.get('username')

        if User.objects.filter(email=email, username=username).exists():
            user = User.objects.get(email=email, username=username)
        else:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)

        send_mail(
            subject='YaMDb регистрация',
            message=f'confirmation_code: {user.confirmation_code}',
            from_email=settings.POST_EMAIL,
            recipient_list=[user.email],
        )
        return response.Response(data=request.data, status=HTTPStatus.OK)


class CustomTokenObtain(generics.CreateAPIView):
    """Представление для создания JWT токена. Имеет только POST запрос.
    """
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.data['username']
        )
        token = serializer.get_token(user)
        return response.Response(
            {'token': f"{ token['access'] }"},
            status=HTTPStatus.OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Пользователя.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    Есть поиск по полю username.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ALLOWED_METHODS

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        serializer_class=UserSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Доступ пользователя к своей учетной записи по '/users/me/'."""
        me_user = request.user
        serializer = self.get_serializer(me_user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                me_user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(email=me_user.email, role=me_user.role)
            return response.Response(
                serializer.data, status=HTTPStatus.OK
            )
        return response.Response(serializer.data, status=HTTPStatus.OK)


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = (Title.objects.all().
                annotate(rating=Avg('reviews__score')).order_by('pk'))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReadTitleSerializer
        return WriteTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_title(self):
        """Получение произведения по id."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())

    def get_queryset(self):
        queryset = self.get_title().reviews.all()
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_review(self):
        """Получение отзыва по id."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())

    def get_queryset(self):
        queryset = self.get_review().comments.all()
        return queryset
