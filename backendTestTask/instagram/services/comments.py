"""
Бизнес-логика работы с комментариями.
"""

from typing import Any
from django.shortcuts import get_object_or_404

# from instagram.models import Post, Comment
# from instagram.api.instagram_api import create_comment as instagram_create_comment

from ..models import Post, Comment
from ..api.instagram_api import create_comment as instagram_create_comment

def create_comment(post_id: int, text: str) -> Comment:
    """
    Создаёт комментарий к посту.

    :param post_id: ID поста в локальной БД
    :param text: текст комментария
    :return: созданный объект Comment
    """
    post: Post = get_object_or_404(Post, pk=post_id)

    response: dict[str, Any] = instagram_create_comment(
        post.instagram_id,
        text,
    )

    return Comment.objects.create(
        post=post,
        text=text,
        instagram_id=response.get("id", ""),
    )