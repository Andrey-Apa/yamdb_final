import csv

from django.core.management.base import BaseCommand

from users.models import User
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


DATA_TUPLE = (
    ('users.csv', User),
    ('category.csv', Category),
    ('genre.csv', Genre),
    ('titles.csv', Title),
    ('genre_title.csv', GenreTitle),
    ('review.csv', Review),
    ('comments.csv', Comment)
)


class Command(BaseCommand):
    """Импортирует тестовые данные из файлов csv в дирректории
    static/data/ в базу данных.
    """
    help = 'Импорт данных в БД из файлов csv.'

    def handle(self, *args, **options):
        for path, model in DATA_TUPLE:
            with open(f'static/data/{path}', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    # При импортировании произведений, необходимо
                    # вместо id категории передать обьект.
                    if path == 'titles.csv':
                        cat_id = row['category']
                        row['category'] = Category.objects.get(pk=cat_id)

                    # При импортировании отзывов и комментариев
                    # вместо id автора передать обьект.
                    if path in ('review.csv', 'comments.csv'):
                        author_id = row['author']
                        row['author'] = User.objects.get(pk=author_id)

                    model.objects.create(**row)
