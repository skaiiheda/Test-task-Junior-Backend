"""
Бизнес-логика работы с постами.
"""

from typing import Any
from django.utils.dateparse import parse_datetime

from backendTestTask.instagram.models import Post
from backendTestTask.instagram.api.instagram_api import InstagramAPI


class PostService:
    """Сервисный слой для работы с постами."""

    @staticmethod
    def sync_posts() -> None:
        """
        Синхронизирует посты из Instagram с локальной БД.

        Алгоритм:
        1. Получить данные из Instagram API
        2. Обновить или создать записи в БД
        """
        posts_data = InstagramAPI.fetch_posts()
        PostService._upsert_posts(posts_data)

    @staticmethod
    def _upsert_posts(posts_data: list[dict[str, Any]]) -> None:
        """
        Создаёт или обновляет посты в базе данных.
        """
        for post_data in posts_data:
            timestamp = parse_datetime(post_data["timestamp"])

            Post.objects.update_or_create(
                instagram_id=post_data["id"],
                defaults={
                    "caption": post_data.get("caption", ""),
                    "media_type": post_data.get("media_type", ""),
                    "media_url": post_data.get("media_url", ""),
                    "permalink": post_data.get("permalink", ""),
                    "timestamp": timestamp,
                },
            )