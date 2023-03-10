import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка поля username модели user на допустимые символы."""

    if re.findall(r'[^\w.@+-]+', value):
        raise ValidationError(
            'Используйте буквы, цифры и символы @/./+/-/ при создании имени.'
        )
