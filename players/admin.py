from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("nickname", "public_id", "created_at")
    search_fields = ("nickname", "public_id")
    readonly_fields = ("public_id", "created_at")