from django.db import models


class Post(models.Model):
    instagram_id = models.CharField(max_length=255, unique=True)
    caption = models.TextField(blank=True)
    media_type = models.CharField(max_length=50)
    media_url = models.URLField(max_length=700)
    permalink = models.URLField(max_length=700)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.instagram_id


class Comment(models.Model):
    instagram_id = models.CharField(max_length=255, unique=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.instagram_id}"