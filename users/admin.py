from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class PostAdmin(admin.ModelAdmin):

    list_display = ("id", "username", "email", "gender")
    list_display_links = ("username", "email")
