from django.db import models


class Post(models.Model):
    instagram_id: str = models.CharField(max_length=255, unique=True)
    caption: str = models.TextField(blank=True)
    media_type: str = models.CharField(max_length=50)
    media_url: str = models.URLField(max_length=700)
    permalink: str = models.URLField(max_length=700)
    timestamp: models.DateTimeField = models.DateTimeField()

    def __str__(self) -> str:
        return self.instagram_id


class Comment(models.Model):
    instagram_id: str = models.CharField(max_length=255, unique=True)
    post: Post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text: str = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment {self.id} on Post {self.post.instagram_id}"
