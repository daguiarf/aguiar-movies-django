from django.conf import settings
from django.db import models

from forum.models import Post

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    LIKE = "like"
    COMMENT = "comment"
    NOTIFICATION_TYPES = [
        (LIKE, "Curtida"),
        (COMMENT, "Comentário"),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="notifications"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def message(self):
        if self.notification_type == self.LIKE:
            return f"{self.sender.username} curtiu seu post"
        return f"{self.sender.username} comentou no seu post"

    def __str__(self):
        return f"[{self.notification_type}] para {self.recipient} de {self.sender}"
