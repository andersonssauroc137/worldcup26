from django.db import models
from players.models import Player
from games.models import Game


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="scores")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scores")

    best_score = models.PositiveIntegerField(default=0)
    last_score = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("player", "game")
        ordering = ["-best_score", "updated_at"]

    def __str__(self):
        return f"{self.player.nickname} - {self.game.title}: {self.best_score}"