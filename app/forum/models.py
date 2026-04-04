from django.conf import settings
from django.db import models

from movies.models import ContentReference

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    """Thread do fórum, associada a um conteúdo TMDB."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_posts")
    content_reference = models.ForeignKey(
        ContentReference, on_delete=models.CASCADE, related_name="forum_posts"
    )
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.content_reference.media_type}] {self.title} by {self.user}"


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} ♥ Post#{self.post_id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} → Post#{self.post_id}"
