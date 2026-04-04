from rest_framework import serializers

from movies.serializers import ContentReferenceSerializer, ContentReferenceWriteSerializer
from .models import Post, PostLike, Comment


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user_username", "content", "created_at"]
        read_only_fields = ["user", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    content_reference = ContentReferenceSerializer(read_only=True)
    content_reference_data = ContentReferenceWriteSerializer(write_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    likes_count = serializers.IntegerField(read_only=True, default=0)
    comments_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Post
        fields = [
            "id", "user_username", "content_reference", "content_reference_data",
            "title", "content", "likes_count", "comments_count",
            "created_at", "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def create(self, validated_data):
        content_serializer = ContentReferenceWriteSerializer(
            data=validated_data.pop("content_reference_data")
        )
        content_serializer.is_valid(raise_exception=True)
        content = content_serializer.get_or_create()
        return Post.objects.create(content_reference=content, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("content_reference_data", None)
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["user", "post", "created_at"]
