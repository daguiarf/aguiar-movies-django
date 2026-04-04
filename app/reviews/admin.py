from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "rating", "created_at"]
    list_filter = ["rating", "content__media_type"]
    search_fields = ["user__username", "content__title"]
    ordering = ["-created_at"]
