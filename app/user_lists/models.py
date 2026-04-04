from django.conf import settings
from django.db import models

from movies.models import ContentReference

User = settings.AUTH_USER_MODEL


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    content = models.ForeignKey(ContentReference, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} ♥ {self.content}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    content = models.ForeignKey(ContentReference, on_delete=models.CASCADE)
    watch_date = models.DateField(null=True, blank=True)
    watched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "content")
        ordering = ["-created_at"]

    def __str__(self):
        status = "✓" if self.watched else "○"
        return f"{self.user} {status} {self.content}"
