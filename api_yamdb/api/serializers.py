from django.shortcuts import get_object_or_404
from django.core.validators import MaxValueValidator, MinValueValidator

from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (User, Category, Genre,
                            GenreTitle, Title, Review, Comment)


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя.
    Проверяет username на запрещенные значения.
    """
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, attrs):
        """Проверка уникальности полей и ввода недопустимого имени 'me'."""
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Поле username не может быть "me".'
            )
        if attrs.get('username') == attrs.get('email'):
            raise serializers.ValidationError(
                'Поля email и username не должны совпадать.'
            )
        return attrs


class CustomTokenObtainSerializer(serializers.ModelSerializer):
    """Сериализатор формы предоставления данных для аутентификации.
    Валидация по "confirmation_code".
    """
    username_field = User.USERNAME_FIELD
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )

    def get_token(self, user):
        """Функция создания токена."""
        access = AccessToken.for_user(user)
        return {'access': str(access), }

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if confirmation_code != str(user.confirmation_code):
            raise serializers.ValidationError('Ошибка ввода данных')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения данных пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class WriteTitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для запросов записи."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        """Добавление связи произведение-жанр (many-to-many)."""
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            GenreTitle.objects.create(title=title, genre=genre)

        return title


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для запросов чтения."""
    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating',
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!'),
        )
    )

    class Meta:
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if (self.context['request'].method == 'POST'
                and Review.objects.filter(author=user,
                                          title=title_id).exists()):
            raise serializers.ValidationError(
                'Вы уже оставили свой отзыв на это произведение!'
            )
        return data
