from rest_framework import serializers

from movies.serializers import ContentReferenceSerializer, ContentReferenceWriteSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    content = ContentReferenceSerializer(read_only=True)
    content_data = ContentReferenceWriteSerializer(write_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "user_username", "content", "content_data",
            "text", "rating", "created_at", "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def create(self, validated_data):
        content_serializer = ContentReferenceWriteSerializer(data=validated_data.pop("content_data"))
        content_serializer.is_valid(raise_exception=True)
        content = content_serializer.get_or_create()
        return Review.objects.create(content=content, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("content_data", None)
        instance.text = validated_data.get("text", instance.text)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.save()
        return instance
