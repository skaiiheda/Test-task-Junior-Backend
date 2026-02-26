import pytest
from rest_framework.test import APIClient
from instagram.models import Post


@pytest.mark.django_db
class TestPostsAPI:
    """
    Тесты работы с постами.
    """

    def test_list_posts(self, api_client: APIClient) -> None:
        """
        Проверяет получение списка постов.
        """

        Post.objects.create(
            instagram_id="post_1",
            caption="test",
            media_type="IMAGE",
            media_url="http://test.com/img.jpg",
            permalink="http://test.com/post",
            timestamp="2024-01-01T00:00:00Z",
        )

        response = api_client.get("/api/posts/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_sync_posts(
            self,
            api_client: APIClient,
            monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """
        Проверяет синхронизацию постов.
        """

        def mock_fetch_posts() -> list[dict]:
            return [
                {
                    "id": "inst_1",
                    "caption": "hello",
                    "media_type": "IMAGE",
                    "media_url": "http://img.jpg",
                    "permalink": "http://post",
                    "timestamp": "2024-01-01T00:00:00Z",
                }
            ]

        monkeypatch.setattr(
            "instagram.services.posts.fetch_posts",
            mock_fetch_posts,
        )

        response = api_client.post("/api/sync/")

        assert response.status_code == 200
        assert Post.objects.count() == 1
