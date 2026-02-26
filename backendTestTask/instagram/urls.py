from django.urls import path
from instagram.views import SyncPostsView, PostListView, CommentCreateView

urlpatterns = [
    path('sync/', SyncPostsView.as_view(), name='sync-posts'),
    path('posts/', PostListView.as_view(), name='list-posts'),
    path('posts/<int:id>/comment/', CommentCreateView.as_view(), name='comment-post'),
]