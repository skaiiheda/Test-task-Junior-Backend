# import pytest
# from rest_framework.test import APIClient
# from unittest.mock import patch
# from ..models import Post, Comment
#
#
# pytestmark = pytest.mark.django_db
#
#
# class TestCommentCreateAPI:
#
#     def setup_method(self):
#         self.client = APIClient()
#
#     # ------------------------------------------------
#     # SUCCESS CASE
#     # ------------------------------------------------
#
#     @patch("instagram.services.InstagramService.post_comment")
#     def test_create_comment_success(self, mock_post_comment):
#         """
#         Проверяет:
#         - комментарий создаётся в БД
#         - API возвращает 201
#         """
#
#         mock_post_comment.return_value = {"id": "inst_comment_123"}
#
#         post = Post.objects.create(
#             instagram_id="inst_post_1",
#             caption="test",
#             media_type="IMAGE",
#             media_url="http://test.com/img.jpg",
#             permalink="http://test.com/post",
#             timestamp="2024-01-01T00:00:00Z",
#         )
#
#         response = self.client.post(
#             f"/api/posts/{post.id}/comment/",
#             {"text": "Hello"},
#             format="json"
#         )
#
#         assert response.status_code == 201
#         assert Comment.objects.count() == 1
#
#         comment = Comment.objects.first()
#         assert comment.text == "Hello"
#         assert comment.instagram_id == "inst_comment_123"
#         assert comment.post == post
#
#     # ------------------------------------------------
#     # POST NOT IN LOCAL DB
#     # ------------------------------------------------
#
#     def test_post_not_found_in_local_db(self):
#         """
#         Проверяет:
#         - если поста нет в БД → 404
#         """
#
#         response = self.client.post(
#             "/api/posts/999/comment/",
#             {"text": "Hello"},
#             format="json"
#         )
#
#         assert response.status_code == 404
#         assert Comment.objects.count() == 0
#
#     # ------------------------------------------------
#     # POST NOT FOUND IN INSTAGRAM
#     # ------------------------------------------------
#
#     @patch("instagram.services.InstagramService.post_comment")
#     def test_post_not_found_in_instagram(self, mock_post_comment):
#         """
#         Проверяет:
#         - если Instagram вернул ошибку "не найден"
#         - комментарий НЕ создаётся
#         """
#
#         from ..services_del import InstagramNotFoundError
#
#         mock_post_comment.side_effect = InstagramNotFoundError()
#
#         post = Post.objects.create(
#             instagram_id="deleted_inst_post",
#             caption="test",
#             media_type="IMAGE",
#             media_url="http://test.com/img.jpg",
#             permalink="http://test.com/post",
#             timestamp="2024-01-01T00:00:00Z",
#         )
#
#         response = self.client.post(
#             f"/api/posts/{post.id}/comment/",
#             {"text": "Hello"},
#             format="json"
#         )
#
#         assert response.status_code == 404
#         assert Comment.objects.count() == 0
