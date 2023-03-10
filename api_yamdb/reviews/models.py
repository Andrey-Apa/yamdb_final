from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

User = get_user_model()

CLS_NAME_LEN: int = settings.CLS_NAME_LEN
FIRST_BOOK_YEAR: int = settings.FIRST_BOOK_YEAR
CURRENT_YEAR: int = int(timezone.now().year)
GENRES_NUM_SHOW: int = settings.GENRES_NUM_SHOW


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        'slug-адрес категории',
        unique=True,
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        'slug-адрес жанра',
        unique=True,
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        'Название произведения',
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(
            MinValueValidator(
                FIRST_BOOK_YEAR,
                'Год выпуска не должен быть меньше 868.'),
            MaxValueValidator(
                CURRENT_YEAR,
                'Год выпуска не должен быть больше текущего.'),
        )
    )
    description = models.TextField(
        'Описание',
        blank=True, null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:CLS_NAME_LEN]

    def display_genre(self):
        """Создает строковое представление жанров для админки."""
        return ', '.join(
            [genre.name for genre in self.genre.all()[:GENRES_NUM_SHOW]])

    display_genre.short_description = 'Жанр'


class GenreTitle(models.Model):
    """Модель для поля many-to-many."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Жанр произведений'
        verbose_name_plural = 'Жанры произведений'
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title'),
        )

    def __str__(self) -> str:
        return f'Произведение {self.title} в жанре {self.genre}'


class Review(models.Model):
    """Описание модели отзывов на произведения."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Оставьте свой отзыв о произведении'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше 1!'),
            MaxValueValidator(10, 'Оценка не может быть больше 10!'),
        ),
        help_text='Укажите вашу оценку в диапазоне от 1 до 10'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            ),
        )

    def __str__(self) -> str:
        return (f'Пользователь {self.author} '
                f'оставил отзыв {self.text[:CLS_NAME_LEN]}')


class Comment(models.Model):
    """Модель комментариев к отзыву."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Оставьте свой комментарий к отзыву'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:CLS_NAME_LEN]
