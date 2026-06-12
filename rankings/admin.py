from django.contrib import admin
from .models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "game",
        "best_score",
        "last_score",
        "attempts",
        "updated_at",
    )
    list_filter = ("game",)
    search_fields = ("player__nickname", "game__title")
    readonly_fields = ("created_at", "updated_at")