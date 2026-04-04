from django.contrib import admin
from .models import Post, PostLike, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "content_reference", "created_at"]
    list_filter = ["content_reference__media_type"]
    search_fields = ["title", "user__username", "content_reference__title"]
    ordering = ["-created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    ordering = ["-created_at"]


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
