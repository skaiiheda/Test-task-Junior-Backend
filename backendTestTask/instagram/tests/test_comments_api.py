import pytest
from rest_framework.test import APIClient
from instagram.models import Post, Comment
from instagram.exceptions import InstagramAPIError


@pytest.mark.django_db
class TestCommentCreateAPI:
    """
    Тесты создания комментариев через API.
    """

    def test_create_comment_success(
            self,
            api_client: APIClient,
            monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """
        Проверяет:
        - комментарий создаётся
        - возвращается 201
        """

        def mock_create_comment(instagram_id: str, text: str) -> dict[str, str]:
            return {"id": "inst_comment_123"}

        monkeypatch.setattr(
            "instagram.services.comments.instagram_create_comment",
            mock_create_comment,
        )

        post = Post.objects.create(
            instagram_id="inst_post_1",
            caption="test",
            media_type="IMAGE",
            media_url="http://test.com/img.jpg",
            permalink="http://test.com/post",
            timestamp="2024-01-01T00:00:00Z",
        )

        response = api_client.post(
            f"/api/posts/{post.id}/comment/",
            {"text": "Hello"},
            format="json",
        )

        assert response.status_code == 201
        assert Comment.objects.count() == 1

        comment = Comment.objects.first()
        assert comment is not None
        assert comment.text == "Hello"
        assert comment.instagram_id == "inst_comment_123"
        assert comment.post == post

    def test_post_not_found_in_local_db(
            self,
            api_client: APIClient,
    ) -> None:
        """
        Если поста нет — Django вернёт 404.
        """

        response = api_client.post(
            "/api/posts/999/comment/",
            {"text": "Hello"},
            format="json",
        )

        assert response.status_code == 404
        assert Comment.objects.count() == 0

    def test_instagram_api_error(
            self,
            api_client: APIClient,
            monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """
        Если Instagram API бросает ошибку —
        API возвращает 400.
        """

        def mock_create_comment(instagram_id: str, text: str) -> dict:
            raise InstagramAPIError("Instagram error")

        monkeypatch.setattr(
            "instagram.services.comments.instagram_create_comment",
            mock_create_comment,
        )

        post = Post.objects.create(
            instagram_id="inst_post_1",
            caption="test",
            media_type="IMAGE",
            media_url="http://test.com/img.jpg",
            permalink="http://test.com/post",
            timestamp="2024-01-01T00:00:00Z",
        )

        response = api_client.post(
            f"/api/posts/{post.id}/comment/",
            {"text": "Hello"},
            format="json",
        )

        assert response.status_code == 400
        assert Comment.objects.count() == 0
