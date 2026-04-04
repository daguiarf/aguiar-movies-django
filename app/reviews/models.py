from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from movies.models import ContentReference

User = settings.AUTH_USER_MODEL


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    content = models.ForeignKey(ContentReference, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "content")
        ordering = ["-created_at"]

    def __str__(self):
        rating_str = f" ★{self.rating}" if self.rating else ""
        return f"{self.user} → {self.content}{rating_str}"
