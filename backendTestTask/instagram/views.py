# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, generics
# from rest_framework.pagination import CursorPagination
# from .models import Post, Comment
# from .serializers import PostSerializer, CommentSerializer
# from .services import InstagramService, InstagramNotFoundError, InstagramAPIError
#
#
# class PostCursorPagination(CursorPagination):
#     """
#     Курсорная пагинация для постов.
#     Пагинирует по полю timestamp (дата публикации поста).
#     """
#     page_size = 10
#     ordering = ('-timestamp', '-id')  # сортировка по убыванию времени публикации
#
#
# class SyncPostsView(APIView):
#     """
#     Эндпоинт для синхронизации всех постов с Instagram.
#     """
#
#     def post(self, request):
#         try:
#             posts_data = InstagramService.fetch_posts()
#             InstagramService.upsert_posts(posts_data)
#             return Response({'status': 'ok'}, status=status.HTTP_200_OK)
#         except InstagramAPIError as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# class PostListView(generics.ListAPIView):
#     """
#     Эндпоинт для получения списка постов с пагинацией.
#     """
#     queryset = Post.objects.all().order_by('-timestamp')
#     serializer_class = PostSerializer
#     pagination_class = PostCursorPagination
#
#
# class CommentCreateView(APIView):
#     """
#     Эндпоинт для создания комментария к посту.
#     """
#
#     def post(self, request, id):
#         try:
#             post = Post.objects.get(pk=id)
#         except Post.DoesNotExist:
#             return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         text = request.data.get('text')
#         if not text:
#             return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             result = InstagramService.post_comment(post.instagram_id, text)
#             comment = Comment.objects.create(
#                 post=post,
#                 text=text,
#                 instagram_id=result.get('id', '')  # сохраняем ID комментария от Instagram
#             )
#             serializer = CommentSerializer(comment)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except InstagramNotFoundError:
#             return Response(
#                 {'error': 'Post not found in Instagram'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except InstagramAPIError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import CursorPagination

# from instagram.models import Post
# from instagram.serializers import PostSerializer, CommentSerializer
from .models import Post
from .serializers import PostSerializer, CommentSerializer
from .services.posts import PostService
from .services.comments import CommentService
# from instagram.services.posts import PostService
# from instagram.services.comments import CommentService
from .exceptions import InstagramAPIError


# from instagram.exceptions import InstagramAPIError


class PostCursorPagination(CursorPagination):
    """Курсорная пагинация по timestamp."""
    page_size = 10
    ordering = ("-timestamp", "-id")


class SyncPostsView(APIView):
    """Эндпоинт синхронизации постов."""

    def post(self, request):
        try:
            PostService.sync_posts()
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
            comment = CommentService.create_comment(id, text)
            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except InstagramAPIError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
