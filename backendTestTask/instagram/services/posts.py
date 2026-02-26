"""
Бизнес-логика работы с постами.
"""

from typing import Any
from django.utils.dateparse import parse_datetime

# from instagram.models import Post
# from instagram.api.instagram_api import fetch_posts
from ..models import Post
from ..api.instagram_api import fetch_posts


def sync_posts() -> None:
    """
    Синхронизирует посты из Instagram с локальной БД.

    Получает данные через Instagram Graph API
    и выполняет upsert (update_or_create) для каждого поста.
    """
    posts_data: list[dict[str, Any]] = fetch_posts()
    _upsert_posts(posts_data)


def _upsert_posts(posts_data: list[dict[str, Any]]) -> None:
    """
    Создаёт или обновляет посты в базе данных.

    :param posts_data: список словарей с данными постов Instagram
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