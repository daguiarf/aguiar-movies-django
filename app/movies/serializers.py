from rest_framework import serializers
from .models import ContentReference


class ContentReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentReference
        fields = ["id", "tmdb_id", "media_type", "title", "poster_path"]


class ContentReferenceWriteSerializer(serializers.Serializer):

    tmdb_id = serializers.IntegerField()
    media_type = serializers.ChoiceField(choices=ContentReference.MEDIA_TYPE_CHOICES)
    title = serializers.CharField(max_length=500)
    poster_path = serializers.CharField(max_length=255, allow_null=True, required=False)

    def get_or_create(self):
        data = self.validated_data
        content, _ = ContentReference.objects.get_or_create(
            tmdb_id=data["tmdb_id"],
            media_type=data["media_type"],
            defaults={"title": data["title"], "poster_path": data.get("poster_path")},
        )
        return content
