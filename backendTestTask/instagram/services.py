import os
import requests
from typing import List, Dict
from .models import Post
from django.utils.dateparse import parse_datetime

ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
BASE_URL = 'https://graph.instagram.com/me/media'


# ---------------------------
# Кастомные исключения
# ---------------------------
class InstagramAPIError(Exception):
    """Общая ошибка при работе с Instagram API"""
    pass


class InstagramNotFoundError(InstagramAPIError):
    """Ошибка: объект Instagram не найден"""
    pass


class InstagramService:
    @staticmethod
    def fetch_posts() -> List[Dict]:
        """
        Получение всех постов пользователя с пагинацией.
        """
        posts = []
        url = f"{BASE_URL}?fields=id,caption,media_type,media_url,permalink,timestamp&access_token={ACCESS_TOKEN}"
        while url:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception(f"Error fetching posts: {resp.text}")
            data = resp.json()
            posts.extend(data.get('data', []))
            url = data.get('paging', {}).get('next')
        return posts

    @staticmethod
    def upsert_posts(posts_data: List[Dict]) -> None:
        """
        Сохраняем или обновляем посты в локальной БД.
        """
        for p in posts_data:
            timestamp = parse_datetime(p['timestamp'])
            Post.objects.update_or_create(
                instagram_id=p['id'],
                defaults={
                    'caption': p.get('caption', ''),
                    'media_type': p.get('media_type', ''),
                    'media_url': p.get('media_url', ''),
                    'permalink': p.get('permalink', ''),
                    'timestamp': timestamp,
                }
            )

    @staticmethod
    def post_comment(instagram_post_id: str, text: str) -> Dict:
        """
        Отправка комментария через Instagram API.
        Возвращает JSON с ID комментария.
        """
        url = f"https://graph.instagram.com/{instagram_post_id}/comments"
        resp = requests.post(url, data={'message': text, 'access_token': ACCESS_TOKEN})
        if resp.status_code == 404:
            raise InstagramNotFoundError("Instagram post not found")

        if resp.status_code != 200:
            raise InstagramAPIError(resp.text)
        return resp.json()
