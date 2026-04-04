from django.contrib import admin
from .models import ContentReference


@admin.register(ContentReference)
class ContentReferenceAdmin(admin.ModelAdmin):
    list_display = ["tmdb_id", "media_type", "title", "poster_path"]
    list_filter = ["media_type"]
    search_fields = ["title", "tmdb_id"]
