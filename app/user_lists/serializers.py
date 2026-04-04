from rest_framework import serializers

from movies.models import ContentReference
from movies.serializers import ContentReferenceSerializer, ContentReferenceWriteSerializer
from .models import Favorite, Watchlist


class FavoriteSerializer(serializers.ModelSerializer):
    content = ContentReferenceSerializer(read_only=True)
    content_data = ContentReferenceWriteSerializer(write_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "content", "content_data", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        content_serializer = ContentReferenceWriteSerializer(data=validated_data.pop("content_data"))
        content_serializer.is_valid(raise_exception=True)
        content = content_serializer.get_or_create()
        return Favorite.objects.create(content=content, **validated_data)


class WatchlistSerializer(serializers.ModelSerializer):
    content = ContentReferenceSerializer(read_only=True)
    content_data = ContentReferenceWriteSerializer(write_only=True)

    class Meta:
        model = Watchlist
        fields = ["id", "content", "content_data", "watch_date", "watched", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]

    def create(self, validated_data):
        content_serializer = ContentReferenceWriteSerializer(data=validated_data.pop("content_data"))
        content_serializer.is_valid(raise_exception=True)
        content = content_serializer.get_or_create()
        return Watchlist.objects.create(content=content, **validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("content_data", None)
        instance.watch_date = validated_data.get("watch_date", instance.watch_date)
        instance.watched = validated_data.get("watched", instance.watched)
        instance.save()
        return instance
