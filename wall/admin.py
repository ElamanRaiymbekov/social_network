from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from wall.models import Post, Comment, Like, Rating


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Посты"""
    list_display = ("user", "published", "create_date", "view_count", "id")


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin, admin.ModelAdmin):
    """ Коментарии к постам"""
    list_display = ("user", "post", "created_date", "update_date", "published", "id")
    mptt_level_indent = 15


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Лайки"""
    list_display = ('user', 'post', 'like')
    list_display_links = ('user', 'post', 'like')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'rating')
    list_display_links = ('user', 'post')
