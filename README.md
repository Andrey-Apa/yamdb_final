# Проект YaMDb API Final
Это групповой учебный проект Яндекс-Практикум
## Описание

Проект YaMDb позволяет через простые запросы API собирать отзывы, оценки и комментарии пользователей на различные произведения хранящиеся в базе данных.

## Технологии
- Python 3.7.9 и выше
- Django 3.2
- Django REST Framework 3.12.4
- SimpleJWT 4.7.2
- Django filter 22.1
- Gunicorn 20.0.4
- Nginx 1.21.3
- Docker 20.10.22
- Postgres 13.0
- Dotenv 0.21.1

## Запуск проекта в контейнере
1. Склонируйте репозиторий и прейдите в корневую директорию:
```bash
git clone git@github.com:Andrey-Apa/api_yamdb.git

cd api_yamdb
```
2. В директории infra создайте файл с .env с переменными окружения:
```bash
cd infra
```

# Содержание .env 
- DB_ENGINE - движок базы данных # например django.db.backends.postgresql
- DB_NAME - имя базы данных # postgres
- POSTGRES_USER - логин для подключения к базе данных # postgres
- POSTGRES_PASSWORD - пароль для подключения к БД (установите свой) # postgres
- DB_HOST - название сервиса (контейнера) # db
- DB_PORT - порт для подключения к БД # 5432
- SECRET_KEY - секретный ключ
- ALLOWED_HOSTS - разрешенные хосты # localhost

3. Соберите контейнер и запустите:
```bash
docker-compose up --build
```
4. В случае необходимости, можно заполнить базу тестовыми данными при помощи команды:
```bash
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
5. Внутри контейнера web выполните миграции, создйте суперпользователя и собертите статику:
```bash
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input 
```

## Документация к API
Подробная документация приведена по ссылке ниже:
http://localhost/redoc

## Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

## Примеры запросов
- GET http://localhost/api/v1/titles/

Возвращает список всех произведений.
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": []
    }
]
```
- POST http://localhost/api/v1/titles/

Создание нового объекта произведения (доступно только админу, суперюзеру).
В теле запроса можно передвать переменные:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
              {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
- GET http://localhost/api/v1/titles/{titles_id}/

Возвращает информацию о конкретном произведении по id (доступно без токена)
Пример ответа:
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
              {}
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
- PATCH, DELETE http://localhost/api/v1/titles/{titles_id}/

Частичное изменение или удаление конкретного объекта (доступно только админу, суперюзеру)
Пример запроса для PATCH:
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
- GET http://localhost/api/v1/titles/1/reviews/

Возвращает список всех отзывов (доступно без токена)
Пример ответа:
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
                {}
    ]
}
```
- POST http://localhost/api/v1/titles/{title_id}/reviews/

Добавление нового отзыва. Пользователь может оставить только один отзыв на произведение и поставить оценку в диапазоне от 1 до 10 (доступно аутентифицированным пользователям)
Пример запроса:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
- GET http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Возварщает список всех комментариев к отзыву по id произведения и отзыва (доступно без токена)
Пример ответа:
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
                {}
    ]
}
```
- POST http://localhost/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Добавление нового комментария к отзыву (доступно аутентифицированным пользователям)
Пример запроса:
```
{
  "text": "string"
}
```
Возвращает индекс и текст комментария, а также имя автора и дату публикации:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2023-01-28T22:15:22Z"
}
```

## Над проектом работали

- Андрей Грицай - https://github.com/Netsky-29
- Максим Бойко - https://github.com/Boikomp
- Андрей Апашкин - https://github.com/Andrey-Apa

## License

MIT

**Free Software, Not for commercial use!**