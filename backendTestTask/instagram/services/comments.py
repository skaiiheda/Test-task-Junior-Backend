"""
Бизнес-логика работы с комментариями.
"""

from typing import Any
from django.shortcuts import get_object_or_404

from backendTestTask.instagram.models import Post, Comment
from backendTestTask.instagram.api.instagram_api import InstagramAPI


class CommentService:
    """Сервисный слой для комментариев."""

    @staticmethod
    def create_comment(post_id: int, text: str) -> Comment:
        """
        Создаёт комментарий к посту.

        Логика:
        1. Проверяем существование поста в БД
        2. Отправляем комментарий в Instagram
        3. Сохраняем комментарий локально
        """
        post: Post = get_object_or_404(Post, pk=post_id)

        response: dict[str, Any] = InstagramAPI.create_comment(
            post.instagram_id,
            text,
        )

        return Comment.objects.create(
            post=post,
            text=text,
            instagram_id=response.get("id", ""),
        )