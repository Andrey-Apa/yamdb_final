from django.contrib import admin

from .models import Category, Title, Genre, GenreTitle, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description',
        'category', 'display_genre'
    )
    list_editable = ('category',)
    list_filter = ('category', 'year')
    search_fields = ('description',)
    empty_value_display = '-пусто-'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre')
    list_filter = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'score', 'author', 'pub_date')
    search_fields = ('author__username', 'text',)
    list_filter = ('title', 'score',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author',)
    empty_value_display = '-пусто-'
