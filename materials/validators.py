from rest_framework.serializers import ValidationError


def validate_forbidden_urls(value):
    """Проверка на допустимые URL"""

    if 'https://www.youtube.com' not in value:
        raise ValidationError("Можно прикреплять видео только с домена youtube.com")

