from django.contrib import admin

from common.admin import LIST_PER_PAGE_SIZE
from posts.models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at")
    ordering = ("-created_at",)

    raw_id_fields = ("user",)
    search_fields = ("id", "title", "user__id")

    list_per_page = LIST_PER_PAGE_SIZE


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    ordering = ("-created_at",)

    raw_id_fields = ("user", "post")
    search_fields = ("id", "user__id", "post__id")

    list_per_page = LIST_PER_PAGE_SIZE
