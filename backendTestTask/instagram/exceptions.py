"""
Кастомные исключения для Instagram-интеграции.
"""


class InstagramAPIError(Exception):
    """Общая ошибка при работе с Instagram API."""
    pass


class InstagramNotFoundError(InstagramAPIError):
    """Объект Instagram не найден."""
    pass