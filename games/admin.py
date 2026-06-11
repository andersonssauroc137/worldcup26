from django.contrib import admin
from .models import Country, Game


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("flag", "name", "code")
    search_fields = ("name", "code")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "country", "platform", "is_published", "created_at")
    list_filter = ("platform", "is_published", "country")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}