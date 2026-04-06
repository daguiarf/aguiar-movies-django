from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.CharField(read_only=True)
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "message",
            "sender_username",
            "post_id",
            "post_title",
            "is_read",
            "created_at",
        ]
        read_only_fields = fields
