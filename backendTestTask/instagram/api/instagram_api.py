"""
Модуль для работы с Instagram Graph API.
Содержит исключительно HTTP-запросы.
"""

from typing import Any
import requests
from django.conf import settings

# from instagram.exceptions import InstagramAPIError, InstagramNotFoundError
from ..exceptions import InstagramNotFoundError, InstagramAPIError

def fetch_posts() -> list[dict[str, Any]]:
    """
    Получает все посты пользователя с пагинацией.

    :return: список словарей с данными постов
    :raises InstagramAPIError: при ошибке ответа API
    """
    posts: list[dict[str, Any]] = []

    url: str | None = (
        f"{settings.INSTAGRAM_BASE_URL}"
        f"?fields=id,caption,media_type,media_url,permalink,timestamp"
        f"&access_token={settings.INSTAGRAM_ACCESS_TOKEN}"
    )

    while url:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise InstagramAPIError(response.text)

        data: dict[str, Any] = response.json()
        posts.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")

    return posts


def create_comment(post_id: str, text: str) -> dict[str, Any]:
    """
    Отправляет комментарий к посту Instagram.

    :param post_id: Instagram ID поста
    :param text: текст комментария
    :return: ответ Instagram API
    :raises InstagramNotFoundError: если пост не найден
    :raises InstagramAPIError: при прочих ошибках
    """
    url: str = f"https://graph.instagram.com/{post_id}/comments"

    response = requests.post(
        url,
        data={
            "message": text,
            "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=10,
    )

    if response.status_code == 404:
        raise InstagramNotFoundError("Instagram post not found")

    if response.status_code != 200:
        raise InstagramAPIError(response.text)

    return response.json()
