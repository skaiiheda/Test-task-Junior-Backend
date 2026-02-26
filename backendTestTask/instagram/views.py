from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import CursorPagination

from instagram.models import Post
from instagram.serializers import PostSerializer, CommentSerializer
from instagram.services.comments import create_comment
from instagram.services.posts import sync_posts
from instagram.exceptions import InstagramAPIError


class PostCursorPagination(CursorPagination):
    """Курсорная пагинация по timestamp."""
    page_size = 10
    ordering = ("-timestamp", "-id")


class SyncPostsView(APIView):
    """Эндпоинт синхронизации постов."""

    def post(self, request):
        try:
            sync_posts()
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except InstagramAPIError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PostListView(generics.ListAPIView):
    """Список постов с пагинацией."""
    queryset = Post.objects.all().order_by("-timestamp")
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination


class CommentCreateView(APIView):
    """Создание комментария."""

    def post(self, request, id: int):
        text: str | None = request.data.get("text")

        if not text:
            return Response(
                {"error": "Text is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            comment = create_comment(id, text)
            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except InstagramAPIError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
